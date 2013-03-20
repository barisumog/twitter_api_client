#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# twitter_api_client
#
# Copyright (C) 2013 barisumog at gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


import string
import random
import time
import urllib.parse
import urllib.request
import hmac
import hashlib
import base64
import json
import sys      # only used for printing when run as script


# The below dictionary must be filled with the consumer and
# access token details for your own app.

KEYCHAIN = {"consumer_key": "--change me--",
            "consumer_secret": "--change me--",
            "access_token": "--change me--",
            "access_token_secret": "--change me--"}


# A few utility functions first:

def nonce(size=30):
    """Generate a random nonce string."""
    valid_chars = string.ascii_letters + string.digits
    nonce_list = []
    while size > 0:
        nonce_list.append(random.choice(valid_chars))
        size -= 1
    return "".join(nonce_list)


def timestamp():
    """Generate current timestamp string."""
    return "{}".format(int(time.time()))


def percent_encode(text):
    """Percent encode a given string."""
    return urllib.parse.quote(text, safe="")


def percent_sort(dictionary, pattern, separator):
    """Generate a string from a given dictionary.

    Percent encode the key:value pairs in the dictionary, and sort the
    encoded keys. Combine each key:value into a single string, according to
    the format given in pattern. Finally, concatenate these strings by
    inserting the given separator between each one."""
    encoded = {}
    for key in dictionary:
        encoded[percent_encode(key)] = percent_encode(dictionary[key])
    sorted_list = []
    for key in sorted(encoded.keys()):
        sorted_list.append(pattern.format(key, encoded[key]))
    return separator.join(sorted_list)


# Now we can create all the OAuth headers, except the signature.

def oauth_init():
    """Generate a dictionary with the OAuth header values."""
    return {"oauth_consumer_key": KEYCHAIN["consumer_key"],
            "oauth_token": KEYCHAIN["access_token"],
            "oauth_nonce": nonce(),
            "oauth_timestamp": timestamp(),
            "oauth_signature_method": "HMAC-SHA1",
            "oauth_version": "1.0"}


# To calculate the signature, we also need the other details
# from the API call.

def oauth_signature(base_url, method, params, post_data, oauth):
    """Calculate the OAuth signature."""
    # Detailed explanation of the steps is given at:
    # https://dev.twitter.com/docs/auth/creating-signature
    combined_dict = {}
    combined_dict.update(params)
    combined_dict.update(post_data)
    combined_dict.update(oauth)
    parameter_str = percent_sort(combined_dict, "{}={}", "&")
    base_str = "&".join([method, percent_encode(base_url), percent_encode(parameter_str)])
    signing_key = "{}&{}".format(KEYCHAIN["consumer_secret"], KEYCHAIN["access_token_secret"])
    hasher = hmac.new(signing_key.encode(), base_str.encode(), hashlib.sha1)
    return base64.b64encode(hasher.digest()).strip()


# The main API call function that wraps all these.

def api_call(base_url, method, params, post_data={}):
    """Make a call to the Twitter API, returning the JSON response."""
    oauth = oauth_init()
    oauth["oauth_signature"] = oauth_signature(base_url, method, params, post_data, oauth)
    auth_header = "OAuth " + percent_sort(oauth, '{}="{}"', ", ")
    if params:
        url = "{}?{}".format(base_url, percent_sort(params, "{}={}", "&"))
    else:
        url = base_url
    if post_data:
        data = percent_sort(post_data, "{}={}", "&").encode()
    else:
        data = None
    headers = {"Authorization": auth_header}
    request = urllib.request.Request(url, data, headers, method=method)
    response = urllib.request.urlopen(request).read()
    return json.loads(response.decode())


# A printer to be used when run as script

def careful_print(text):
    """Prints text, checking for unicode errors."""
    try:
        print(text)
    except UnicodeEncodeError:
        ptext = "{}\n".format(text).encode()
        sys.stdout.buffer.write(ptext)


if __name__ == "__main__":
    # Just a quick test to retrieve the current TTs.
    # Since the TTs could contain characters not included in
    # the default system encoding, so using the above printer
    # function. Occasional garbled text is expected. =)
    print("Requesting the Trending Topics...")
    base_url = "https://api.twitter.com/1.1/trends/place.json"
    method = "GET"
    params = {"id": "1"}    # worldwide TTs
    response = api_call(base_url, method, params)
    for tt in response[0]["trends"]:
        careful_print(tt["name"])
