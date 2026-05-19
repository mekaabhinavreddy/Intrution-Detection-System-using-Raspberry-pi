import time
import sys
from scapy.all import sniff
from scapy.layers.inet import IP
from colorama import Fore, Style

# Initialize variables
packet_count = 0
start_time = time.time()
last_alert_time = 0  # cooldown
ip_counter = {}      # store IP counts

def process_packet(packet):
    global packet_count, start_time, last_alert_time, ip_counter

    # ✅ Ignore non-IP packets (fixes "Unknown")
    if not packet.haslayer(IP):
        return

    packet_count += 1

    # Get source IP
    src_ip = packet[IP].src
    ip_counter[src_ip] = ip_counter.get(src_ip, 0) + 1

    # Check every 1 second
    if time.time() - start_time >= 1:
        packets_per_sec = packet_count

        # 🔥 Find top attacker IP
        if ip_counter:
            attacker_ip = max(ip_counter, key=ip_counter.get)
        else:
            attacker_ip = "No IP"

        # 🔴 ATTACK DETECTION
        if packets_per_sec > 120:
            if time.time() - last_alert_time > 3:
                last_alert_time = time.time()

                # 🔔 Beep sound
                sys.stdout.write('\a')
                sys.stdout.flush()

                # 🔴 Alert message
                print(Fore.RED + f"[ALERT] DoS Attack from {attacker_ip}: {packets_per_sec} packets/sec 🚨" + Style.RESET_ALL)

                # 📝 Logging
                with open("alerts.log", "a") as f:
                    f.write(f"{time.ctime()} | DoS from {attacker_ip}: {packets_per_sec} packets/sec\n")

        # 🟢 NORMAL TRAFFIC
        else:
            if packets_per_sec < 10:
                status = "LOW"
            elif packets_per_sec < 100:
                status = "NORMAL"
            else:
                status = "HIGH"

            print(Fore.GREEN + f"[INFO] {status} Traffic: {packets_per_sec} packets/sec (Top IP: {attacker_ip})" + Style.RESET_ALL)

        # Reset counters
        packet_count = 0
        ip_counter = {}
        start_time = time.time()


# 🚀 START MONITORING
print(Fore.CYAN + "[INFO] Real-Time IDS Started on wlan0..." + Style.RESET_ALL)

sniff(iface="wlan0", filter="ip", prn=process_packet, store=0)