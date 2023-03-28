#!/usr/bin/env python3
# Author: Gary Hooks
# Date: March 2023
# Licence: GPLv3
# Version 2.0

import requests
import json
import sys
from colorama import Fore, Style
from prettytable import PrettyTable

def ipqualityscore(danger_threshold, ip):
    api_key = "YOUR API KEY"
    url = "https://ipqualityscore.com/api/json/ip/" + api_key + "/" + ip + "?strictness=0&allow_public_access_points=true&fast=true&lighter_penalties=true&mobile=true"

    response = requests.request(method="GET", url=url)
    decodedResponse = json.loads(response.text)

    if decodedResponse["fraud_score"] >= danger_threshold:
        return True
    else:
        return False

def scamalytics(danger_threshold, ip):
    api_key = "YOUR API KEY"
    url = "https://api11.scamalytics.com/garyhooks/?key=" + api_key + "&ip=" + ip

    response = requests.request(method="GET", url=url)
    decodedResponse = json.loads(response.text)

    if decodedResponse["credits"]["remaining"] < 25:
        print("[!] Running Low on credits, less than 25 remaining")


    if decodedResponse["score"] >= danger_threshold:
        return True
    else:
        return False

def abuseipdb(danger_threshold, max_days, ip):
    ## Register here to obtain your own API key: https://www.abuseipdb.com/login
    api_key = "YOUR API KEY"
    url = 'https://api.abuseipdb.com/api/v2/check'

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

    if decodedResponse["data"]["abuseConfidenceScore"] >= danger_threshold:
        return True
    else:
        return False


def output_results(bad_ips):
        print(Fore.RED + "\n[+] Tabular results of Bad IPs:")
        print("-----------------------------------------------------------------------")
        print(Style.RESET_ALL)

        table = PrettyTable()
        table.field_names = ["IP", "AbuseIPDB", "Scamalytics", "ipqualityscore"]
        table.align = "l"
        for record in bad_ips.values():
            table.add_row(
                [
                    record["ip"],
                    record["abuseipdb"],
                    record["scamalytics"],
                    record["ipqualityscore"]
                ]
            )

        print(table)

        print(Fore.RED + "\n[+] CSV List:")
        print("-----------------------------------------------------------------------")
        print(Style.RESET_ALL)

        print("ip,abuseipdb,abuseipdb-URL, scamalytics, scamalytics-URL, ipqualityscore, ipqualityscore-URL, Google")
        for record in bad_ips.values():
            print(record["ip"] + "," +
                  str(record["abuseipdb"]) + "," +
                  "https://www.abuseipdb.com/check/" + record["ip"] + "," +
                  str(record["scamalytics"]) + "," +
                  "https://scamalytics.com/ip/" + record["ip"] + "," +
                      str(record["ipqualityscore"]) + "," +
                  "https://www.ipqualityscore.com/free-ip-lookup-proxy-vpn-test/lookup/" + record["ip"] + "," +
                    "https://www.google.com/search?q=" + record["ip"]
                    )

        print(Style.RESET_ALL)

        print(Fore.RED + "\n[+] Plain Text list of bad IPs shown below:")
        print("-----------------------------------------------------------------------")
        print(Style.RESET_ALL)

        for record in bad_ips.values():
            print(record["ip"])

        print(Style.RESET_ALL + "\n")


if __name__ == "__main__":
    danger_threshold = 50
    ## Abuse IPDB: How many days to search over. Min=1, Default=30, Max=365
    max_days = 90

    bad_ips = {}
    counter = 0

    ip_list = open("ips.txt", "r")
    for line in ip_list:
        ip = line.strip()

        bad_ips[counter] = { "ip" : ip,
                        "abuseipdb" : abuseipdb(danger_threshold, max_days, ip),
                        "scamalytics" : scamalytics(danger_threshold, ip),
                        "ipqualityscore" : ipqualityscore(danger_threshold, ip)
                        }
        counter += 1


    output_results(bad_ips)
