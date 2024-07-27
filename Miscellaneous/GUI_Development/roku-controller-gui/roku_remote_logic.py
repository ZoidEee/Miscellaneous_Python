import socket
import ipaddress
import concurrent.futures
import requests

class RokuController:
    def __init__(self):
        self.devices = []

    def scan_network(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()

        network = ipaddress.IPv4Network(f"{local_ip}/24", strict=False)

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            future_to_ip = {executor.submit(self._scan_ip, ip): ip for ip in network.hosts()}
            for future in concurrent.futures.as_completed(future_to_ip):
                try:
                    result = future.result()
                    if result:
                        self.devices.append(result)
                except Exception as e:
                    ip = future_to_ip[future]
                    print(f"Error processing result for {ip}: {str(e)}")

    def _scan_ip(self, ip):
        try:
            with socket.create_connection((str(ip), 8060), timeout=1):
                response = requests.get(f"http://{ip}:8060/query/device-info", timeout=2)
                if response.status_code == 200:
                    info = response.text
                    name = info.split("<friendly-device-name>")[1].split("</friendly-device-name>")[0]
                    return {'ip': str(ip), 'name': name}
        except (socket.timeout, ConnectionRefusedError, requests.RequestException):
            pass
        except Exception as e:
            print(f"Unexpected error scanning {ip}: {str(e)}")
        return None
    def _send_command(self, ip, command):
        try:
            response = requests.post(f"http://{ip}:8060/{command}", timeout=5)
            if response.status_code == 200:
                return f"Success: {response.status_code}"
            else:
                return f"Failed: {response.status_code}"
        except requests.RequestException as e:
            return f"Error: {str(e)}"

    def list_apps(self, ip):
        try:
            response = requests.get(f"http://{ip}:8060/query/apps", timeout=2)
            if response.status_code == 200:
                return response.text
            else:
                return f"Failed to list apps: {response.status_code}"
        except requests.RequestException as e:
            return f"Error: {str(e)}"