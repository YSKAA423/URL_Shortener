"""
This function works with CUTTLY'S API
to retrive the shortened version of the url

requests library will be used to "request"
the url via the API service at CUTTLY

The documentation at https://cutt.ly/api-documentation/regular-api

from the documentation:

URL Shortener
To shorten the link, open the file https://cutt.ly/api/api.php remotely (eg via the php file_get_contents), 
and in the parameters: short enter the address to be shortened (it should be encoded so any special characters will be interpreted correctly),
 name specify the preferred shortening of the link, userDomain specify if you want to use your own domain, to do so send 1.

Note: 
          - A status code of 7 means success
          
          - A status of 3 will be sent if the name has been used in their system,
              hence why they should as unique as possible

          

Caution: The service's free tier has a limited number of requests per month so keep that in mind.
"""

import requests
import json
from config import API_KEY



def shorten_url(long_url, name_to_use):
     
    base_url = "https://cutt.ly/api/api.php"
    # remember key, short, and name are the keys required
    body = {'key': API_KEY, 'short': long_url, 'name':name_to_use}

    try:
        response = requests.get(base_url, params=body)  
        data = response.json()  
        print(f"API response: {data}")  # Full response

        if data['url']['status'] == 7:
            short_link = data['url']['shortLink']
            print(f"Success \n Short Url: {short_link} \n")
        else:
            print(f"Failed to shorten URL, status code: {data['url']['status']} \n")
    except Exception as e:
        print(f"An error has occurred: {str(e)}")
        print("Response content:", response.text if response else "No response")

shorten_url("https://www.youtube.com/watch?v=-g41MUVhGL0","meow") # an example


