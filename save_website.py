#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 23:02:11 2024

@author: joy
"""

import tldextract
from urllib.parse import urlparse

# Define the function to extract the domain
def extract_domain(url):
    # Check if the URL starts with a scheme, if not, add one
    if not url.startswith(('http://', 'https://', 'ftp://')):
        url = 'http://' + url

    url = url.replace(':///', '://')
    try:
        result = urlparse(url)
        if result.netloc:
            # URL is valid, proceed with extraction
            extracted = tldextract.extract(url)
            if extracted.domain and extracted.suffix:
                return f"{extracted.domain}.{extracted.suffix}"
            else:
                return -3  # Invalid domain or suffix
        else:
            return -2  # Invalid netloc
    except ValueError:
        return -1  # Invalid URL