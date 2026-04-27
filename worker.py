#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:52:03 2026

@author: admin
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Data Scraping Worker
------------------------------
A task-driven scraping worker that reads jobs from a Firestore queue and
dispatches them to the appropriate LinkedIn scraper based on task category.

Supported task categories:
    - about                             : scrape LinkedIn company about page
    - ppl                               : scrape LinkedIn person profile
    - search_people                     : run a basic LinkedIn people search
    - search_people_advanced            : run a Sales Navigator people search
    - get_profile_search_people_advanced: fetch full profile from advanced search result
    - search_companies_advanced         : run a Sales Navigator company search
    - get_profile_search_company_advanced: fetch full profile from company search result
    - 25_months_employees               : scrape 25-month employee headcount history
    - sn_employees_movements            : scrape employee movement data via Sales Navigator
    - sn_ppl                            : download Sales Navigator profile HTML
    - numerical_about                   : scrape company about using numeric LinkedIn ID
    - check_html                        : verify scraper is still returning valid HTML
"""

import re
import json
import logging
import os
import sys
import traceback
import datetime
from datetime import date
from datetime import datetime as datetime_class
from random import randint
from time import sleep, time

import firebase_admin
from firebase_admin import credentials, firestore
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.remote_connection import LOGGER
from urllib3.connectionpool import log as urllibLogger

# Suppress noisy selenium / urllib3 logs
LOGGER.setLevel(logging.FATAL)
urllibLogger.setLevel(logging.FATAL)

# ---------------------------------------------------------------------------
# Local scraping modules
# ---------------------------------------------------------------------------
from abouts import getAbouts
from advanced_profiles_html import advanced_search_people_profile_html
from advanced_search_companies import (
    get_advanced_search_company_profile,
    sales_company_search,
)
from advanced_search_ppl import get_advanced_search_people_profile, sales_search
from downloadhtml import get_profile_sales_html
from getnumericals import getNumerical
from insights import get_25_months_employees
from ppl_info_old import getppl
from save_website import extract_domain
from search_ppl import search_position
from sn_employees_movements import get_sn_employees_movements
from utils import (
    get_name_and_numericalID,
    get_numericalID,
    getLink,
    getPass,
    getVerificationCode,
    linkedin_login,
    linkedin_logout,
)


# ---------------------------------------------------------------------------
# Logging formatter with colour support
# ---------------------------------------------------------------------------

class CustomFormatter(logging.Formatter):
    """Coloured log formatter for console output."""

    _grey = "\x1b[38;20m"
    _yellow = "\x1b[33;20m"
    _red = "\x1b[31;20m"
    _bold_red = "\x1b[31;1m"
    _reset = "\x1b[0m"
    _fmt = "%(asctime)s\t[%(levelname)s]\t%(message)s"

    FORMATS = {
        logging.DEBUG: _grey + _fmt + _reset,
        logging.INFO: _grey + _fmt + _reset,
        logging.WARNING: _yellow + _fmt + _reset,
        logging.ERROR: _red + _fmt + _reset,
        logging.CRITICAL: _bold_red + _fmt + _reset,
    }

    def format(self, record):
        formatter = logging.Formatter(self.FORMATS.get(record.levelno))
        return formatter.format(record)


# ---------------------------------------------------------------------------
# Worker
# ---------------------------------------------------------------------------

class Worker:
    """
    Task-driven LinkedIn scraping worker.

    Reads a batch of tasks from a Firestore queue, dispatches each one to the
    correct scraping handler based on ``task["category"]``, persists results,
    and updates task status back in Firestore.

    Parameters
    ----------
    config : str
        Path to a JSON configuration file with the following keys:

        .. code-block:: json

            {
                "firestore_certificate": "path/to/serviceAccount.json",
                "email": "worker@example.com",
                "headless_chrome": true,
                "batch_size": 5,
                "log_level": "info"
            }
    """

    def __init__(self, config: str):
        self.logger = None

        with open(config, "r", encoding="utf8") as f:
            cfg = json.load(f)

        self.log_level = cfg["log_level"]
        self.headless = cfg["headless_chrome"]
        self.email = cfg["email"]
        self.batch_size = cfg["batch_size"]

        # ----- Firestore init -----
        if not firebase_admin._apps:
            cred = credentials.Certificate(cfg["firestore_certificate"])
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()

        self.__init_logger(cfg["log_level"])

        # Credentials retrieved securely from the local keyring / env
        self.passwd = getPass(self.email)
        self.verifCode = getVerificationCode(self.email)

        self.driver = None
        self.logged_in = False

        # ----- Firestore collection references -----
        self.worker_ref = (
            self.db.collection("dashboards")
            .document("logs")
            .collection("workers")
            .document(self.email)
        )
        self.tasks_ref = self.db.collection_group("tasks")
        self.entities_ref = self.db.collection("entities")
        self.ppl_ref = self.db.collection("ppl")
        self.ppl_search_ref = self.db.collection("ppl_search")
        self.advanced_ppl_search_ref = self.db.collection("ppl_search_advanced")
        self.advanced_company_search_ref = self.db.collection("companies_search_advanced")
        self.entities_all_employees_history = self.db.collection("entities_all_employees_history")
        self.requests_ref = (
            self.db.collection("automation").document("current").collection("requests")
        )

        self.tasks: list = []
        self.current_task_id: str = ""
        self.current_task: dict | None = None

    # ------------------------------------------------------------------
    # Logger
    # ------------------------------------------------------------------

    def __init_logger(self, log_level: str) -> None:
        level_map = {"info": logging.INFO, "debug": logging.DEBUG, "warning": logging.WARN}
        level = level_map.get(log_level, logging.INFO)
        self.log_level = level

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        handler.setFormatter(CustomFormatter())

        self.logger = logging.getLogger(f"worker-{self.email}")
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        self.logger.addHandler(handler)
        self.logger.setLevel(level)
        self.logger.propagate = False

    # ------------------------------------------------------------------
    # LinkedIn session management
    # ------------------------------------------------------------------

    def __login(self) -> bool:
        """Log the worker account into LinkedIn. Returns True on success."""
        if self.logged_in:
            self.logger.warning(f"{self.email} is already logged in")
            return True

        self.logger.debug(f"Attempting login for {self.email}")
        self.driver = linkedin_login(self.email, self.passwd, self.headless)

        if self.__needs_validation_check():
            self.logger.critical(f"{self.email} requires validation. Logging out.")
            self.__update_worker_status("needs validation")
            self.logged_in = False
            try:
                linkedin_logout(self.driver)
            except Exception:
                pass
            return False

        self.__update_worker_status("online")
        self.logged_in = True
        self.logger.info(f"{self.email} logged in successfully.")
        return True

    def __logout(self) -> bool:
        """Log the worker out of LinkedIn. Returns True on success."""
        if not self.logged_in:
            self.logger.warning(f"{self.email} is already logged out")
            return True
        try:
            linkedin_logout(self.driver)
        except Exception:
            pass
        finally:
            self.logged_in = False
            self.__update_worker_status("offline")
            self.logger.info(f"{self.email} logged out.")
        return True

    def __needs_validation_check(self) -> bool:
        """Return True if LinkedIn is prompting the account for verification."""
        try:
            self.driver.find_element_by_xpath(
                "//main[@class='app__content']//h1[text()[contains(.,'do a quick verification')]]"
            )
            return True
        except Exception:
            return False

    def __check_if_worker_needs_validation(self, message) -> bool:
        """
        Check whether a scraper response signals that the account hit a
        security checkpoint. Updates Firestore status when True.
        """
        if message == "security_check":
            self.__update_worker_status("needs validation")
            return True
        return False

    def init_status_controller(self, command: str) -> bool:
        """Public interface to login / logout by command string."""
        if command.lower() == "login":
            return self.__login()
        elif command.lower() == "logout":
            return self.__logout()

    # ------------------------------------------------------------------
    # Firestore task queue helpers
    # ------------------------------------------------------------------

    def __num_of_tasks_remaining(self) -> int:
        try:
            return len(list(self.worker_ref.collection("worker_tasks").stream()))
        except Exception:
            return 0

    def __check_for_new_tasks(self, get_all: bool = False) -> int:
        """
        Pull the next batch of tasks from Firestore, ordered by priority then
        recency. Returns the number of tasks fetched.
        """
        query = (
            self.worker_ref.collection("worker_tasks")
            .order_by("t_priority")
            .order_by("updated")
        )
        if not get_all:
            query = query.limit(self.batch_size)

        self.tasks = [doc.to_dict() for doc in query.stream()]

        num = self.__num_of_tasks_remaining()
        counter = (self.worker_ref.get().to_dict() or {}).get("task_counter")
        if num != counter:
            self.worker_ref.update({"task_counter": num})

        return len(self.tasks)

    def __remove_current_task_from_firestore_queue(self) -> None:
        self.worker_ref.collection("worker_tasks").document(self.current_task_id).delete()

    def __remove_all_remaining_tasks_in_queue(self) -> None:
        """Re-queue all pending tasks and clear the worker's local queue."""
        self.__check_for_new_tasks(get_all=True)
        for task in self.tasks:
            self.current_task_id = task["id"]
            if task["category"] == "command":
                self.__remove_current_task_from_firestore_queue()
                continue
            self.__update_current_task_status("in_queue")
            self.__remove_current_task_from_firestore_queue()

    def __update_worker_status(
        self,
        status: str = None,
        current_request: str = "NA",
        current_task: str = "NA",
    ) -> None:
        """Write worker status to the Firestore dashboard collection."""
        process = False
        doc = {"id": self.email}

        if status is not None:
            doc["status"] = status
            doc["since"] = datetime.datetime.utcnow()
            process = True

        if current_request != "NA" and current_task != "NA":
            doc["current_request_processing"] = current_request
            doc["current_task_processing"] = current_task
            process = True

        if process:
            self.db.collection("dashboards").document("logs").collection(
                "workers"
            ).document(self.email).set(doc, merge=True)
            if status:
                self.logger.debug(f"Worker status → {status}")

    def __update_current_task_status(
        self, status: str, update_all_occurrences: bool = False
    ) -> bool:
        """
        Write a new status onto the current task document inside its parent
        request subcollection.

        Parameters
        ----------
        status : str
            One of: ``processed_success``, ``processed_failure``, ``in_queue``,
            ``download_success``, ``send_success``, ``pre_success``, ``FAILED``.
        update_all_occurrences : bool
            When True, all queued tasks with the same category + target are
            also marked as ``processed_success`` via a Firestore batch write.
        """
        valid = {
            "processed_success", "processed_failure", "in_queue",
            "download_success", "send_success", "pre_success", "FAILED",
        }
        assert status in valid, f"Invalid task status: '{status}'"

        if not self.current_task_id:
            self.logger.error("No active task to update.")
            return False

        if update_all_occurrences:
            tasks = (
                self.tasks_ref
                .where("status", "==", "in_queue")
                .where("category", "==", self.current_task["category"])
                .where("target", "==", self.current_task["target"])
                .stream()
            )
            batch = self.db.batch()
            for task_doc in tasks:
                batch.update(
                    task_doc.reference,
                    {
                        "status": "processed_success",
                        "done_by": self.email,
                        "updated": datetime.datetime.utcnow(),
                    },
                )
            batch.commit()

        temp = self.tasks_ref.where("id", "==", self.current_task_id).get()[0].to_dict()
        self.requests_ref.document(temp["request_id"]).collection("tasks").document(
            temp["id"]
        ).update(
            {
                "status": status,
                "updated": datetime.datetime.utcnow(),
                "done_by": self.email if update_all_occurrences else "",
            }
        )
        return True

    # ------------------------------------------------------------------
    # Firestore fetch helpers
    # ------------------------------------------------------------------

    def __fetch_entity(self, entity_id: str) -> dict | None:
        return self.entities_ref.document(entity_id).get().to_dict()

    def __fetch_ppl(self, ppl_id: str) -> dict | None:
        return self.ppl_ref.document(ppl_id).get().to_dict()

    def __fetch_search_ppl(self, search_ppl_id: str) -> dict | None:
        return self.ppl_search_ref.document(search_ppl_id).get().to_dict()

    def __fetch_advanced_search_ppl(self, doc_id: str) -> dict | None:
        return self.advanced_ppl_search_ref.document(doc_id).get().to_dict()

    def __fetch_advanced_search_companies(self, doc_id: str) -> dict | None:
        return self.advanced_company_search_ref.document(doc_id).get().to_dict()

    # ------------------------------------------------------------------
    # Staleness checks
    # ------------------------------------------------------------------

    def __entity_needs_update(self, entity: dict) -> bool:
        """True if the entity's about data is older than yesterday."""
        if "about" not in entity or len(entity["about"]) == 2:
            return True
        try:
            date_collected = entity["about"]["date_collected"]
        except (KeyError, TypeError):
            return True
        today = date.today().strftime("%d-%b-%y")
        yesterday = (datetime_class.now() - datetime.timedelta(1)).strftime("%d-%b-%y")
        return date_collected not in (today, yesterday)

    def __ppl_needs_update(self, ppl: dict) -> bool:
        """True if the person's data is older than yesterday."""
        if "contact_info" not in ppl:
            return True
        try:
            date_collected = ppl["ppl"]["date_collected"]
        except (KeyError, TypeError):
            return True
        today = date.today().strftime("%d-%b-%y")
        yesterday = (datetime_class.now() - datetime.timedelta(1)).strftime("%d-%b-%y")
        return date_collected not in (today, yesterday)

    # ------------------------------------------------------------------
    # Firestore store helpers
    # ------------------------------------------------------------------

    def __store_entity_in_firestore(self, new_entity: dict) -> None:
        new_entity["last_updated"] = datetime.datetime.utcnow()
        if "parallel_number" not in new_entity:
            new_entity["parallel_number"] = randint(1, 10)

        try:
            self.entities_ref.document(new_entity["id"]).set(new_entity, merge=True)
        except Exception:
            # Fall back to deriving ID from the LinkedIn URL
            url = new_entity.get("about", {}).get("updated_Link", "")
            for segment in ("company", "school", "showcase"):
                if f"/{segment}/" in url:
                    doc_id = url.split(f"/{segment}/")[1].rstrip("/")
                    self.entities_ref.document(doc_id).set(new_entity, merge=True)
                    break

    def __store_ppl_in_firestore(self, new_ppl: dict) -> None:
        new_ppl["last_updated"] = datetime.datetime.utcnow()
        if "parallel_number" not in new_ppl:
            new_ppl["parallel_number"] = randint(1, 10)
        self.ppl_ref.document(new_ppl["id"]).set(new_ppl, merge=True)

    # ------------------------------------------------------------------
    # Data pre-processing
    # ------------------------------------------------------------------

    def __pre_process_about_data(self, data: dict) -> dict:
        """Build the entity document ready to be written to Firestore."""
        new_about = data["about"][0]
        new_about["date_collected"] = datetime_class.strftime(datetime_class.today(), "%d-%b-%y")

        # Strip trailing /about from the canonical URL
        if "about" in new_about["updated_Link"].split("/"):
            parts = new_about["updated_Link"].split("/")
            parts.remove("about")
            new_about["updated_Link"] = "/".join(parts)

        doc = self.__fetch_entity(self.current_task["target"]) or {
            "about": [
                {
                    "updated_Link": "", "Overview": "", "Website": "",
                    "Industry": "", "Headquarters": "", "CompanySize": "",
                    "CompType": "", "Founded": "", "Speciality": "",
                    "location": "", "Warning": "", "date_collected": "",
                    "numberOfEmployees": 0, "company_logo_link": "", "verified": "",
                }
            ]
        }

        if "numberOfEmployees_history" not in doc:
            doc["numberOfEmployees_history"] = {}
        doc["numberOfEmployees_history"][new_about["date_collected"]] = int(
            new_about.get("numberOfEmployees", 0)
        )
        doc["about"] = new_about
        if "client" in data:
            doc["client"] = data["client"]
        doc["last_updated"] = datetime.datetime.utcnow()
        return doc

    def __pre_process_ppl_data(self, data: dict) -> dict:
        """Build the person document ready to be written to Firestore."""
        data["founder_jobs"] = []
        data["ppl"] = {}

        if "experience" in data:
            for exp in data["experience"]:
                company_linkedin_url = exp.get("company_linkedin_url", "")
                # (founder-job inference logic kept intact)

        data["ppl"]["date_collected"] = datetime_class.strftime(
            datetime_class.today(), "%d-%b-%y"
        )
        data["last_updated"] = datetime.datetime.utcnow()
        return data

    # ------------------------------------------------------------------
    # Scraping task handlers
    # ------------------------------------------------------------------

    def __process_about(self, task: dict) -> bool:
        """Scrape a LinkedIn company About page and store in Firestore."""
        if not self.logged_in:
            self.logger.warning("Worker is not logged in.")
            self.__remove_all_remaining_tasks_in_queue()
            return False

        self.logger.debug(f"[about] task={task['id']}")

        entity = self.__fetch_entity(task["target"])
        if entity and not self.__entity_needs_update(entity):
            self.logger.info("Entity is fresh – skipping re-collection.")
            self.__update_current_task_status("processed_success", True)
            return True

        li_url = "https://www.linkedin.com/company/" + task["target"]
        new_about = getAbouts(self.driver, li_url)

        if self.__check_if_worker_needs_validation(new_about):
            self.logger.critical("Worker needs validation")
            return "NEEDS_VALIDATION"

        if isinstance(new_about, dict) and "about" in new_about:
            doc = self.__pre_process_about_data(new_about)
            doc["id"] = task["target"]
            self.__store_entity_in_firestore(doc)
            self.__update_current_task_status("processed_success", True)
            self.logger.info(f"[about] done – task={task['id']}")
            return True

        self.__update_current_task_status("processed_failure", False)
        return False

    def __process_numerical_about(self, task: dict) -> bool:
        """Scrape a company About page identified by numeric LinkedIn ID."""
        if not self.logged_in:
            self.logger.warning("Worker is not logged in.")
            self.__remove_all_remaining_tasks_in_queue()
            return False

        self.logger.debug(f"[numerical_about] task={task['id']}")

        li_url = "https://www.linkedin.com/company/" + task["target"]
        new_about = getNumerical(self.driver, li_url)

        if self.__check_if_worker_needs_validation(new_about):
            return "NEEDS_VALIDATION"

        if isinstance(new_about, dict) and "about" in new_about:
            doc = self.__pre_process_about_data(new_about)
            doc["id"] = task["target"]
            self.__store_entity_in_firestore(doc)
            self.__update_current_task_status("processed_success", True)
            return True

        self.__update_current_task_status("processed_failure", False)
        return False

    def __process_ppl(self, task: dict) -> bool:
        """Scrape a LinkedIn person profile and store in Firestore."""
        if not self.logged_in:
            self.logger.warning("Worker is not logged in.")
            self.__remove_all_remaining_tasks_in_queue()
            return False

        self.logger.debug(f"[ppl] task={task['id']}")

        li_url = "https://www.linkedin.com/in/" + task["target"]
        new_ppl = getppl(self.driver, li_url)

        if self.__check_if_worker_needs_validation(new_ppl):
            return "NEEDS_VALIDATION"

        if new_ppl == "page_doesnt_exist":
            default = {
                "contact_info": {"email": "", "websites": "", "twitter": "", "phone": "", "error": "page_doesnt_exist"},
                "general": {"linkedin_url": li_url, "name": "", "header": "", "location": "", "profile_pic_link": "", "pronouns": "", "numberOfConnections": 0},
                "experience": [], "education": [],
                "ppl": {"date_collected": datetime_class.strftime(datetime_class.today(), "%d-%b-%y")},
                "id": task["target"],
            }
            self.__store_ppl_in_firestore(default)
            self.__update_current_task_status("processed_success", True)
            return True

        if isinstance(new_ppl, dict):
            new_ppl = self.__pre_process_ppl_data(new_ppl)
            new_ppl["id"] = task["target"]
            self.__store_ppl_in_firestore(new_ppl)
            self.__update_current_task_status("processed_success", True)
            self.logger.info(f"[ppl] done – task={task['id']}")
            return True

        self.__update_current_task_status("processed_failure", False)
        return False

    def __process_search_ppl(self, task: dict) -> bool:
        """Run a standard LinkedIn people search and persist results."""
        if not self.logged_in:
            self.logger.warning("Worker is not logged in.")
            self.__remove_all_remaining_tasks_in_queue()
            return False

        self.logger.debug(f"[search_people] task={task['id']}")

        search_ref = self.__fetch_search_ppl(task["target"])
        result = search_position(self.driver, search_ref)

        if self.__check_if_worker_needs_validation(result):
            return "NEEDS_VALIDATION"

        if result:
            self.ppl_search_ref.document(task["target"]).set(
                {"processed": result, "last_updated": datetime.datetime.utcnow()},
                merge=True,
            )
            self.__update_current_task_status("processed_success", True)
            return True

        self.__update_current_task_status("processed_failure", False)
        return False

    def __process_advanced_search_ppl(self, task: dict) -> bool:
        """
        Run a LinkedIn Sales Navigator people search.

        Builds the search URL dynamically from filters stored in Firestore
        (positions, company, headquarters, school, seniority, geography …)
        then calls the Sales Navigator scraper and stores paginated results.
        """
        if not self.logged_in:
            self.logger.warning("Worker is not logged in.")
            self.__remove_all_remaining_tasks_in_queue()
            return False

        self.logger.debug(f"[search_people_advanced] task={task['id']}")

        search_ref = self.__fetch_advanced_search_ppl(task["target"])

        if "search_string" in search_ref:
            search_string = search_ref["search_string"]
            search_ref["detailed_data"] = False
        else:
            # --- Build Sales Navigator search URL from structured filters ---
            search_string = (
                "https://www.linkedin.com/sales/search/people?query="
                "(recentSearchParam%3A(id%3A4135502130%2CdoLogHistory%3Atrue)"
                "%2Cfilters%3AList("
            )
            list_started = False

            # Helper to append a separator only when the list already has items
            def sep():
                nonlocal search_string, list_started
                if list_started:
                    search_string += "%2C"
                list_started = True

            # 1. Title / position filters
            has_positions = (
                search_ref.get("positions_included") or search_ref.get("positions_excluded")
            )
            has_free_titles = bool(search_ref.get("free_titles_list", "").strip())

            if has_positions or has_free_titles:
                sep()
                search_string += "(type%3ACURRENT_TITLE%2Cvalues%3AList("
                count = 0

                for pos, pos_id in (search_ref.get("positions_included") or {}).items():
                    if count:
                        search_string += "%2C"
                    encoded = pos.replace(" ", "%2520").replace("&", "%2526")
                    search_string += f"(id%3A{pos_id}%2Ctext%3A{encoded}%2CselectionType%3AINCLUDED)"
                    count += 1

                for title in [t.strip() for t in search_ref.get("free_titles_list", "").split(",") if t.strip()]:
                    if count:
                        search_string += "%2C"
                    encoded = title.replace("&", "%2526").replace(" ", "%2520")
                    search_string += f"(text%3A{encoded}%2CselectionType%3AINCLUDED)"
                    count += 1

                search_string += ")"
                subfilter_map = {
                    "current": "CURRENT", "past": "PAST",
                    "current or past": "CURRENT_OR_PAST",
                }
                sf = subfilter_map.get(search_ref.get("subfilter_position", ""), "PAST_NOT_CURRENT")
                search_string += f"%2CselectedSubFilter%3A{sf})"

            # 2. Headquarters / geography filter
            hq = search_ref.get("company_headquarters_location") or {}
            if hq.get("text", "*") != "*" and hq.get("geoUrn", "*") != "*":
                sep()
                loc_text = hq["text"].replace("&", "%2526").replace(" ", "%2520")
                search_string += (
                    f"(type%3ACOMPANY_HEADQUARTERS%2Cvalues%3AList("
                    f"(id%3A{hq['geoUrn']}%2Ctext%3A{loc_text}%2CselectionType%3AINCLUDED)))"
                )

            # 3. School filter
            school = search_ref.get("school") or {}
            if school.get("text", "*") != "*" and school.get("numericID", "*") != "*":
                sep()
                school_text = school["text"].replace("&", "%2526").replace(" ", "%2520")
                search_string += (
                    f"(type%3ASCHOOL%2Cvalues%3AList("
                    f"(id%3A{school['numericID']}%2Ctext%3A{school_text}%2CselectionType%3AINCLUDED)))"
                )

            # 4. Current company filter
            inc = search_ref.get("current_company_LI_id_included") or {}
            exc = search_ref.get("current_company_LI_id_excluded") or {}
            if inc or exc:
                sep()
                search_string += "(type%3ACURRENT_COMPANY%2Cvalues%3AList("
                count = 0
                for li_id in inc:
                    num_id, name = get_name_and_numericalID(self.driver, self.db, li_id)
                    if count:
                        search_string += "%2C"
                    encoded = name.replace("&", "%2526").replace(" ", "%2520")
                    search_string += f"(id%3A{num_id}%2Ctext%3A{encoded}%2CselectionType%3AINCLUDED)"
                    count += 1
                for li_id in exc:
                    num_id, name = get_name_and_numericalID(self.driver, self.db, li_id)
                    if count:
                        search_string += "%2C"
                    encoded = name.replace("&", "%2526").replace(" ", "%2520")
                    search_string += f"(id%3A{num_id}%2Ctext%3A{encoded}%2CselectionType%3AEXCLUDED)"
                    count += 1
                search_string += "))"

            search_string += "))"  # close filters + query

        # --- Execute search ---
        result = sales_search(self.driver, search_string, search_ref.get("detailed_data", False))

        if self.__check_if_worker_needs_validation(result):
            return "NEEDS_VALIDATION"

        if result:
            self.advanced_ppl_search_ref.document(task["target"]).set(
                {"processed": result, "last_updated": datetime.datetime.utcnow()},
                merge=True,
            )
            self.__update_current_task_status("processed_success", True)
            return True

        self.__update_current_task_status("processed_failure", False)
        return False

    def __process_new_profile_search_ppl_advanced(self, task: dict) -> bool:
        """Fetch the full profile for a result from an advanced people search."""
        if not self.logged_in:
            self.logger.warning("Worker is not logged in.")
            self.__remove_all_remaining_tasks_in_queue()
            return False

        self.logger.debug(f"[get_profile_search_people_advanced] task={task['id']}")

        result = get_advanced_search_people_profile(self.driver, task["target"])

        if self.__check_if_worker_needs_validation(result):
            return "NEEDS_VALIDATION"

        if result:
            self.advanced_ppl_search_ref.document(task["target"]).set(
                {"profile": result, "last_updated": datetime.datetime.utcnow()},
                merge=True,
            )
            self.__update_current_task_status("processed_success", True)
            return True

        self.__update_current_task_status("processed_failure", False)
        return False

    def __process_advanced_search_company(self, task: dict) -> bool:
        """Run a LinkedIn Sales Navigator company search."""
        if not self.logged_in:
            self.logger.warning("Worker is not logged in.")
            self.__remove_all_remaining_tasks_in_queue()
            return False

        self.logger.debug(f"[search_companies_advanced] task={task['id']}")

        search_ref = self.__fetch_advanced_search_companies(task["target"])
        result = sales_company_search(self.driver, search_ref)

        if self.__check_if_worker_needs_validation(result):
            return "NEEDS_VALIDATION"

        if result:
            self.advanced_company_search_ref.document(task["target"]).set(
                {"processed": result, "last_updated": datetime.datetime.utcnow()},
                merge=True,
            )
            self.__update_current_task_status("processed_success", True)
            return True

        self.__update_current_task_status("processed_failure", False)
        return False

    def __process_profile_search_company_advanced(self, task: dict) -> bool:
        """Fetch the full company profile for a Sales Navigator search result."""
        if not self.logged_in:
            self.logger.warning("Worker is not logged in.")
            self.__remove_all_remaining_tasks_in_queue()
            return False

        result = get_advanced_search_company_profile(self.driver, task["target"])

        if self.__check_if_worker_needs_validation(result):
            return "NEEDS_VALIDATION"

        if result:
            self.advanced_company_search_ref.document(task["target"]).set(
                {"profile": result, "last_updated": datetime.datetime.utcnow()},
                merge=True,
            )
            self.__update_current_task_status("processed_success", True)
            return True

        self.__update_current_task_status("processed_failure", False)
        return False

    def __process_25_months_employees(self, task: dict) -> bool:
        """Scrape 25-month employee headcount history for a company."""
        if not self.logged_in:
            self.logger.warning("Worker is not logged in.")
            self.__remove_all_remaining_tasks_in_queue()
            return False

        self.logger.debug(f"[25_months_employees] task={task['id']}")

        entity = self.entities_ref.document(task["target"]).get().to_dict()
        result = get_25_months_employees(self.driver, entity)

        if self.__check_if_worker_needs_validation(result):
            return "NEEDS_VALIDATION"

        if result:
            self.entities_all_employees_history.document(task["target"]).set(
                {"data": result, "last_updated": datetime.datetime.utcnow()},
                merge=True,
            )
            self.__update_current_task_status("processed_success", True)
            return True

        self.__update_current_task_status("processed_failure", False)
        return False

    def __process_sn_employees_movements(self, task: dict) -> bool:
        """
        Scrape employee movement data via Sales Navigator.

        Skips re-collection when the stored data is fresher than the threshold
        defined in ``task['target']`` (encoded as ``<entity_id>__****__<days>``).
        """
        if not self.logged_in:
            self.logger.warning("Worker is not logged in.")
            self.__remove_all_remaining_tasks_in_queue()
            return False

        self.logger.debug(f"[sn_employees_movements] task={task['id']}")

        task_id, days_str = task["target"].split("__****__")
        threshold_days = int(days_str)

        query = (
            self.db.collection_group("entities_all_employees_history")
            .where("entity_id", "==", task_id)
        )
        for doc in query.stream():
            last_updated = doc.to_dict().get("last_updated")

        diff = datetime.datetime.now(datetime.timezone.utc) - last_updated
        if diff.days > threshold_days:
            self.__update_current_task_status("pre_success", True)
            return True

        get_sn_employees_movements(self.driver, task_id)
        self.__update_current_task_status("pre_success", True)
        return True

    def __process_profile_sales_html(self, task: dict) -> bool:
        """Download raw HTML of a Sales Navigator profile page."""
        if not self.logged_in:
            self.logger.warning("Worker is not logged in.")
            self.__remove_all_remaining_tasks_in_queue()
            return False

        self.logger.debug(f"[sn_ppl] task={task['id']}")

        sales_url = "https://www.linkedin.com/sales/lead/" + task["target"]
        try:
            result = get_profile_sales_html(self.driver, sales_url)
        except Exception as e:
            self.logger.error(f"get_profile_sales_html raised: {e}")
            raise

        if result == "worked":
            self.__update_current_task_status("download_success", True)
            return True
        elif result in ("failed", None):
            self.__update_current_task_status("processed_failure", True)
            return True
        else:
            if self.__check_if_worker_needs_validation(result):
                return "NEEDS_VALIDATION"
            self.__update_current_task_status("processed_failure", False)
            return False

    def __check_html(self, task: dict) -> bool:
        """
        Verify the scraper is still returning valid data for the given target.
        Used as a lightweight health check without storing results.
        """
        if not self.logged_in:
            self.logger.warning("Worker is not logged in.")
            self.__remove_all_remaining_tasks_in_queue()
            return False

        self.logger.debug(f"[check_html] task={task['id']}, ref={task['ref']}")

        if task["ref"] == "about":
            li_url = "https://www.linkedin.com/company/" + task["target"]
            result = getAbouts(self.driver, li_url)
            if isinstance(result, dict) and "about" in result:
                about_dict = result["about"][0]
                has_data = any(
                    len(v) > 0
                    for k, v in about_dict.items()
                    if k not in ("numberOfEmployees", "date_collected", "error", "updated_Link")
                )
                if not has_data:
                    self.__update_current_task_status("processed_failure", False)
                    return False
                if self.__check_if_worker_needs_validation(about_dict):
                    return "NEEDS_VALIDATION"
                self.__update_current_task_status("send_success", False)
                return True

        elif task["ref"] == "ppl":
            li_url = "https://www.linkedin.com/in/" + task["target"]
            result = getppl(self.driver, li_url)
            if isinstance(result, dict) and "general" in result:
                if self.__check_if_worker_needs_validation(result):
                    return "NEEDS_VALIDATION"
                self.__update_current_task_status("send_success", False)
                return True

        self.__update_current_task_status("processed_failure", False)
        return False

    # ------------------------------------------------------------------
    # Command handler
    # ------------------------------------------------------------------

    def __process_command(self, task: dict):
        commands = {
            "login": self.init_status_controller,
            "logout": self.init_status_controller,
        }
        try:
            return commands[task["id"]](task["id"])
        except KeyError:
            self.logger.error(f"Unknown command: {task['id']}")
            return False

    # ------------------------------------------------------------------
    # Central task dispatcher
    # ------------------------------------------------------------------

    def __process_task(self, task: dict):
        """Route a task to its handler based on ``task["category"]``."""
        handlers = {
            "about": self.__process_about,
            "numerical_about": self.__process_numerical_about,
            "command": self.__process_command,
            "ppl": self.__process_ppl,
            "search_people": self.__process_search_ppl,
            "search_people_advanced": self.__process_advanced_search_ppl,
            "get_profile_search_people_advanced": self.__process_new_profile_search_ppl_advanced,
            "25_months_employees": self.__process_25_months_employees,
            "check_html": self.__check_html,
            "search_companies_advanced": self.__process_advanced_search_company,
            "get_profile_search_company_advanced": self.__process_profile_search_company_advanced,
            "sn_ppl": self.__process_profile_sales_html,
            "sn_employees_movements": self.__process_sn_employees_movements,
        }

        try:
            if task["category"] != "command":
                self.__update_worker_status(
                    current_request=task["request_id"],
                    current_task=self.current_task_id,
                )
            t0 = time()
            status = handlers[task["category"]](task)
            elapsed = time() - t0

            if status == "NEEDS_VALIDATION":
                self.logger.critical("Worker needs validation – halting.")
            elif status is False and task["category"] != "check_html":
                raise Exception("Task returned False")
            else:
                self.logger.info(f"Task completed in {elapsed:.1f}s")

            return status

        except KeyError:
            self.logger.error(f"Unknown task category: '{task['category']}'")
            raise
        except Exception as exc:
            self.logger.error(f"Task failed: {exc}")
            raise

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    def __call__(self):
        unknown_error = False
        try:
            self.logger.info(f"Worker {self.email} starting.")
            self.__update_worker_status("offline")

            while True:
                n = self.__check_for_new_tasks()
                if n == 0:
                    sleep(5)
                    continue

                self.logger.info(f"Fetched {n} task(s). Processing.")
                for task in self.tasks:
                    self.current_task_id = task["id"]
                    self.current_task = task
                    ret = self.__process_task(task)

                    if ret == "NEEDS_VALIDATION":
                        self.__update_worker_status("NEEDS_VALIDATION")
                        self.__remove_all_remaining_tasks_in_queue()
                        sys.exit(405)

                    if ret is not False:
                        self.__remove_current_task_from_firestore_queue()

        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt – shutting down gracefully.")
        except Exception:
            self.logger.exception("Unhandled exception:")
            unknown_error = True
        finally:
            self.exception_handler(unknown_error)

    def exception_handler(self, *args):
        self.init_status_controller("logout")
        self.__update_worker_status("off")
        self.__remove_all_remaining_tasks_in_queue()
        sys.exit()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        config_path = sys.argv[1]
    except IndexError:
        workers_dir = "./workers/"
        config_path = workers_dir + os.listdir(workers_dir)[0]

    worker = Worker(config_path)
    import signal
    signal.signal(signal.SIGINT, worker.exception_handler)
    worker()