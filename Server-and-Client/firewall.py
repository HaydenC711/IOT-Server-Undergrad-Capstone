import socket

# Define firewall rules (for now only HTTP traffic)
ALLOWED_PORTS = [80]  # List of allowed ports

def is_port_allowed(port):
    return port in ALLOWED_PORTS


#def packetFilter(packet):
	#if IP in packet:
		#srcIp = packet[IP].src
		#print("Packet from {srcIP} is safe and can pass through")


def main():
    # Create a socket to capture incoming packets
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))

    while True:
        try:
            # Receive a packet
            packet, addr = sock.recvfrom(65535)

            # Extract the destination port (assuming it's a TCP packet)
            dest_port = int.from_bytes(packet[36:38], byteorder='big')

            if is_port_allowed(dest_port):
                # Allow the packet to pass through
                print(f"Allowed packet with destination port {dest_port}")
            else:
                # Drop the packet (block)
                print(f"Blocked packet with destination port {dest_port}")

        except KeyboardInterrupt:
            break

    # Close the socket when done
    sock.close()


def packetFilter(packet):
	if IP in packet:
		srcIp = packet[IP].src
		print("Packet from {srcIP} is safe and can pass through")














main()

