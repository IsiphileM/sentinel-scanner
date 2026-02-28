# 🛰️ Project Sentinel: Stealth TCP Scanner

### 📋 Overview
Sentinel is a network reconnaissance tool built in Python using the `Scapy` library. It performs **half-open (SYN) scanning**, a technique used by security engineers to map network services without establishing a full TCP connection.

### 🔬 How it Works (The Theory)
This tool follows the **TCP Three-Way Handshake** logic:
1. **SYN Sent:** Sentinel sends a synchronization packet to the target port.
2. **SYN-ACK Received:** If the port is open, the target responds with SYN-ACK. Sentinel identifies this and sends a **RST (Reset)** packet to terminate the connection before it's completed.
3. **RST-ACK Received:** If the port is closed, the target responds with RST-ACK.

### 🛠️ Installation & Usage
```bash
# Install Scapy
pip install -r requirements.txt

# Run the scanner (Requires root/admin privileges for raw packet crafting)
sudo python3 src/sentinel.py 192.168.1.1 80