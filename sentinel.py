import sys
from scapy.all import IP, TCP, sr1
import logging

# Suppress Scapy IPv6 warnings for a cleaner terminal look
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

def sentinel_scan(target_ip, port):
    print(f"[!] PROBING: {target_ip} on PORT: {port}")
    
    # Craft a Stealth SYN Packet
    # IP(dst=target_ip) builds the network layer
    # TCP(dport=port, flags="S") builds the transport layer with SYN flag
    syn_packet = IP(dst=target_ip)/TCP(dport=port, flags="S")
    
    # Send packet and wait for 1 response (timeout 2 seconds)
    response = sr1(syn_packet, timeout=2, verbose=0)
    
    if response is None:
        print(f"[-] PORT {port}: FILTERED (No response/Firewall)")
    elif response.haslayer(TCP):
        if response.getlayer(TCP).flags == 0x12: # 0x12 is SYN-ACK
            print(f"[+] PORT {port}: OPEN (Service Detected)")
            # Send a Reset (RST) packet to close the connection stealthily
            rst_packet = IP(dst=target_ip)/TCP(dport=port, flags="R")
            sr1(rst_packet, timeout=1, verbose=0)
        elif response.getlayer(TCP).flags == 0x14: # 0x14 is RST-ACK
            print(f"[-] PORT {port}: CLOSED")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: sudo python3 sentinel.py <IP> <PORT>")
        sys.exit(1)
    
    target = sys.argv[1]
    port_to_scan = int(sys.argv[2])
    sentinel_scan(target, port_to_scan)