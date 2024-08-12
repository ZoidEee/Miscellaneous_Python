import socket
import ipaddress
import concurrent.futures
import requests


class RokuController:
    def __init__(self):
        self.devices = []

    def scan_network(self):
        # Get the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()

        # Determine the network to scan
        network = ipaddress.IPv4Network(f"{local_ip}/24", strict=False)
        print(f"Scanning network: {network}")

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
            response = requests.post(f"http://{ip}:8060/{command}", timeout=2)
            if response.status_code == 200:
                print(f"Successfully sent command '{command}' to Roku device at {ip}")
            else:
                print(f"Failed to send command '{command}' to Roku device at {ip}, status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error sending command to {ip}: {str(e)}")

    def power_off(self, device):
        self._send_command(device['ip'], "keypress/PowerOff")

    def power_on(self, device):
        self._send_command(device['ip'], "keypress/PowerOn")

    def volume_up(self, device):
        self._send_command(device['ip'], "keypress/VolumeUp")

    def volume_down(self, device):
        self._send_command(device['ip'], "keypress/VolumeDown")

    def mute(self, device):
        self._send_command(device['ip'], "keypress/VolumeMute")

    def home(self, device):
        self._send_command(device['ip'], "keypress/Home")

    def select(self, device):
        self._send_command(device['ip'], "keypress/Select")

    def back(self, device):
        self._send_command(device['ip'], "keypress/Back")

    def play(self, device):
        self._send_command(device['ip'], "keypress/Play")

    def pause(self, device):
        self._send_command(device['ip'], "keypress/Pause")

    def list_devices(self):
        if not self.devices:
            print("No Roku devices found.")
        else:
            print("Found Roku devices:")
            for device in self.devices:
                print(f"- {device['name']} at {device['ip']}")

def main():
    controller = RokuController()
    controller.scan_network()
    controller.list_devices()


    if controller.devices:
        device = controller.devices[0]  # Control the first found device
        print(f"\nControlling {device['name']} at {device['ip']}")
        #controller.volume_up(device)
        #controller.volume_down(device)
        #controller.mute(device)
        #controller.home(device)
        # Uncomment the following line to power off the device
        # controller.power_off(device)

if __name__ == "__main__":
    main()