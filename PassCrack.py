import subprocess
import os
import re
from collections import namedtuple
import configparser
def get_windows_saved_ssids():
    output=subprocess.check_output("netsh wlan show profiles").decode()
    ssids=[]
    profiles=re.findall(r"All User Profiles(.*)",output)
    for profile in profiles:
        ssids=profile.strip().strip(":").strip()
        ssids.append(ssid)
    return ssids
def get_windows_saved_wifi_password(verbose=1):
    ssids=get_windows_saved_ssids()
    Profile=namedtuple("Profile",["ssid","ciphers","key"])
    profiles=[]
    for ssid in ssids:
        ssid_details=subprocess.check_output(f"""netsh wlan show profile"{ssid}"key=clear""").decode()
        ciphers=re.findall(r"Ciphers(.*)",ssid_details)
        ciphers="/".join([c.strip().strip(":").strip() for c in ciphers])
        key=re.findall(r"Key Contents(.*)",ssid_details)
        try:
            key=key[0].strip().strip(":").strip()
        except IndexError:
            key="None"
        profile=Profile(ssid=ssid,ciphers=ciphers,key=key)
        if verbose >=1:
            print_windows_profile(profile)
        profiles.append(profile)
    return profiles
def print_windows_profile(profile):
    print(f"{profile.ssid:25}{profile.ciphers:15}{profile.key:50}")
def print_windows_profiles(verbose):
    print("SSID            CIPHER(S)       KEY ")
    print("-"*50)
    get_windows_saved_wifi_passwords(verbose)
