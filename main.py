#!/usr/bin/env python3
# Author: Gary Hooks
# Date: March 2023
# Licence: GPLv3

import requests
import json
import sys
from colorama import Fore, Style

def main():
    api_key = "PUT YOUR KEY HERE"
    url = 'https://api.abuseipdb.com/api/v2/check'

    ## Minimum "confidence score" to indicate dangerous IP, 100 is the most dangerous
    danger_threshold = 50

    ## How many days to search over. Min=1, Default=30, Max=365
    max_days = 90

    ip_list = open("ips.txt", "r")
    bad_ips = []
    for line in ip_list:
        ip = line.strip()

        querystring = {
            'ipAddress': ip,
            'maxAgeInDays': max_days
        }

        headers = {
            'Accept': 'application/json',
            'Key': api_key
        }

        response = requests.request(method='GET', url=url, headers=headers, params=querystring)
        decodedResponse = json.loads(response.text)

        output = (ip + ": Confidence Score: "
        + str(decodedResponse["data"]["abuseConfidenceScore"]) + " > "
        + str(decodedResponse["data"]["totalReports"]) + " total reports by "
        + str(decodedResponse["data"]["numDistinctUsers"]) + " in the last "
        + str(max_days) + " days")

        if decodedResponse["data"]["abuseConfidenceScore"] > danger_threshold:
            print(Fore.RED + output)
            bad_ips.append(ip)
        else:
            print(Fore.GREEN + output)

    print(Fore.RED + "\n[+] All IPs over threshold of " + str(danger_threshold) + " confidence score are listed below:")
    print("----------------------------------------------------------------------")
    for ip in bad_ips:
        print(Fore.RED + ip)

    print(Style.RESET_ALL + "\n")

if __name__ == "__main__":
    main()
