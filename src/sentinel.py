import sys
from scapy.all import IP, TCP, sr1
import logging

# Suppress Scapy IPv6 warnings for a cleaner terminal look
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

def sentinel_scan(target_ip, port):
    print(f"[!] PROBING: {target_ip} on PORT: {port}")
    
    # Craft a Stealth SYN Packet
    syn_packet = IP(dst=target_ip)/TCP(dport=port, flags="S")
    
    # Send packet and wait (Windows loopback is fast, 0.5s is enough)
    response = sr1(syn_packet, timeout=0.5, verbose=0)
    
    # Safety Check: Did we even get a response?
    if response is None:
        print(f"[-] PORT {port}: FILTERED (No response)")
    elif response.haslayer(TCP):
        flags = response.getlayer(TCP).flags
        if flags == 0x12: # SYN-ACK
            print(f"[+] PORT {port}: OPEN (Service Detected)")
            # Send RST to be polite
            sr1(IP(dst=target_ip)/TCP(dport=port, flags="R"), timeout=0.5, verbose=0)
        elif flags == 0x14: # RST-ACK
            print(f"[-] PORT {port}: CLOSED")

if __name__ == "__main__":
    # Updated to take 3 arguments: IP, START_PORT, END_PORT
    if len(sys.argv) != 4:
        print("Usage: python src/sentinel.py <IP> <START_PORT> <END_PORT>")
        sys.exit(1)
    
    target = sys.argv[1]
    start_p = int(sys.argv[2])
    end_p = int(sys.argv[3])

    print(f"\n--- [SENTINEL SCAN STARTING ON {target}] ---")
    for port in range(start_p, end_p + 1):
        sentinel_scan(target, port)
    print("--- [SCAN COMPLETE] ---\n")