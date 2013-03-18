twitter_api_client
==================

A simple and direct interface to the Twitter APIs in Python 3.

**twitter_api_client** is a concise tool for calling the
Twitter APIs. It's main purpose is testing and CLI scripting,
so it merely handles the OAuth protocol, leaving everything else
as raw as possible. It doesn't wrap the responses into custom objects.
It doesn't obscure the request parameters.

Requirements
------------

**twitter_api_client** works solely on the standard library,
so there are no dependencies.

You must, however, have a valid consumer key and secret,
as well as an access token and secret.

You can create an app at https://dev.twitter.com/apps
. From there, you can obtain your consumer and access token credentials.

Please make sure to setup your app with the appropriate permissions.
If you will be using POST APIs (e.g. tweeting), you must choose the
*read/write* permissions.

Installing
----------

Just copy the **twitter_api_client.py** file to your working
directory.

Make sure you populate the **KEYCHAIN** dictionary at the top
of the file with your own credentials.

Usage
-----

If you just run the file as a script, it should give a (possibly garbled)
list of the current trending topics. If you run into any errors,
something is probably wrong. Feel free to shout out to me, I'd be
glad to help if I can.

The ``api_call(base_url, method, params, post_data={})`` function is the
main interface. The arguments are:

``base_url`` The base url of the API resource. Starts with ``https://``
and ends with ``.json``

``method`` Either **GET** or **POST**. Detailed list of resources
and methods at https://dev.twitter.com/docs/api/1.1

``params`` Dictionary of parameters for **GET** requests.

``post_data`` Dictionary of parameters for **POST** requests. Empty by
default, so can be omitted for GET requests.

All API calls return the full JSON response, converted into a Python
dictionary or list.

Examples
--------

**Global trending topics**

https://dev.twitter.com/docs/api/1.1/get/trends/place

    import twitter_api_client as tac
    base_url = "https://api.twitter.com/1.1/trends/place.json"
    method = "GET"
    params = {"id": "1"}
    response = tac.api_call(base_url, method, params)

**Search for tweets**

https://dev.twitter.com/docs/api/1.1/get/search/tweets

    import twitter_api_client as tac
    base_url = "https://api.twitter.com/1.1/search/tweets.json"
    method = "GET"
    params = {"q": "python", "result_type": "recent", "count": "20"}
    response = tac.api_call(base_url, method, params)

**Post a tweet for the authenticated user**

https://dev.twitter.com/docs/api/1.1/post/statuses/update

    import twitter_api_client as tac
    base_url = "https://api.twitter.com/1.1/statuses/update.json"
    method = "POST"
    params = {}
    post_data = {"status": "I ate my cat for breakfast!"}
    response = tac.api_call(base_url, method, params, post_data)

License
-------

**twitter_api_client** is open sourced under GPLv3.