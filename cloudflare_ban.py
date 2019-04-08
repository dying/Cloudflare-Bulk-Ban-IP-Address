import os
import json
import time
import logging
import requests
import cf_settings

# Get the API credentials from cf_settings.py
CF_API_KEY = cf_settings.api_key
CF_EMAIL = cf_settings.api_email
ZONE_ID = cf_settings.zone_id

# Configure logfile -- comment this out if you don't want a logfile
logging.basicConfig(filename="cloudflare_bans.log", format="%(asctime)s\t%(levelname)s:\t%(message)s", level=logging.INFO)
# TODO: implement logging so that errors can be reviewed later

def post_to_cloudflare(ip_address):                     
    """Post a firewall access rules to the Cloudflare API.
    
    Don't post more than 1,200 times in five minutes.
    
    """

    r = requests.post("https://api.cloudflare.com/client/v4/zones/{}/firewall/access_rules/rules".format(ZONE_ID),
    headers={
        'X-Auth-Key': CF_API_KEY,
        'X-Auth-Email': CF_EMAIL,
    }, json={
            "mode": "js_challenge",
            "configuration": {
                "target": "ip",
                "value": ip_address
            },
            "notes": "This rule as been created by Cloudflare Ban Python Script"
    })
    print("Printing response code: ", r.status_code)

def read_file_and_ban():
    """Reads IP addresses from a file and bans them via Cloudflare."""
    
    f = open('banned_ips.txt')
    for line in f:
        cleaned_line = line.strip()
        print("About to ban:", cleaned_line)
        post_to_cloudflare(cleaned_line)
        time.sleep(0.5) # ensure that it stays under 1,200 requests in five minutes. This limits it to 600.
    f.close()

if __name__ == '__main__':
    read_file_and_ban()

