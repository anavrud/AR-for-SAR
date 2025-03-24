import socket
import threading
import time
import random
import json

def generate_gps_data():
    """Generate simulated GPS data"""
    return {
        "latitude": 63.4305 + random.uniform(-0.001, 0.001), 
        "longitude": 10.3951 + random.uniform(-0.001, 0.001),
        "altitude": 5.0 + random.uniform(0, 10),
        "timestamp": int(time.time() * 1000),
        "valid": True
    }

def handle_client(client_socket):
    """Handle a client connection"""
    try:
        while True:
            # Generate GPS data
            gps_data = generate_gps_data()
            
            # Convert to JSON string
            json_data = json.dumps(gps_data)
            
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
    server_port = 8085  # Using a different port than your image server
    
    server.bind((server_ip, server_port))
    server.listen(5)
    
    print(f"[*] Listening on {server_ip}:{server_port}")
    
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
    start_server()
