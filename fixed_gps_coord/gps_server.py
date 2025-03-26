import socket
import threading
import time
import json
import subprocess
import os

def get_android_gps():
    """Get real GPS data from Android via termux-api"""
    try:
        # Call termux-location command
        output = subprocess.check_output(['termux-location']).decode('utf-8')
        
        # Parse the JSON output
        location_data = json.loads(output)
        
        return {
            "latitude": location_data['latitude'],
            "longitude": location_data['longitude'],
            "altitude": location_data.get('altitude', 0),
            "timestamp": int(time.time() * 1000),
            "valid": True
        }
    except Exception as e:
        print(f"Error getting GPS data: {e}")
        # Return fallback data
        return {
            "latitude": 0.0,
            "longitude": 0.0,
            "altitude": 0.0,
            "timestamp": int(time.time() * 1000),
            "valid": False
        }

def handle_client(client_socket):
    """Handle a client connection"""
    try:
        while True:
            # Get GPS data from Android
            gps_data = get_android_gps()
            
            # Convert to JSON string
            json_data = json.dumps(gps_data)
            
            # Print for debug
            print(f"Sending: {json_data}")
            
            # Send data to client
            message = json_data.encode('utf-8')
            client_socket.send(message)
            
            # Sleep for a second
            time.sleep(1)
    except Exception as e:
        print(f"Connection closed: {e}")
    finally:
        client_socket.close()

def start_server():
    """Start the GPS server"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind to all interfaces
    server_ip = '0.0.0.0'
    server_port = 8085
    
    server.bind((server_ip, server_port))
    server.listen(5)
    
    # Get this device's IP address
    ip_info = subprocess.check_output(['ifconfig', 'wlan0']).decode('utf-8')
    ip_address = "unknown"
    for line in ip_info.split('\n'):
        if "inet " in line:
            ip_address = line.split('inet ')[1].split(' ')[0]
    
    print(f"[*] GPS Server running")
    print(f"[*] IP Address: {ip_address}")
    print(f"[*] Port: {server_port}")
    print(f"[*] Use this in Unity: {ip_address}:{server_port}")
    
    try:
        while True:
            client, addr = server.accept()
            print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
            
            # Create a thread to handle the client
            client_handler = threading.Thread(target=handle_client, args=(client,))
            client_handler.daemon = True
            client_handler.start()
    except KeyboardInterrupt:
        print("[*] Shutting down server")
        server.close()

if __name__ == "__main__":
    # Request location permissions first
    os.system('termux-location')
    print("Starting GPS server...")
    start_server()
