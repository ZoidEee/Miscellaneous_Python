from pycoingecko import CoinGeckoAPI
import menu3
import smtplib
from email.mime.text import MIMEText
import schedule
import time
import getpass

class CoinLister:
    def __init__(self):
        self.cg = CoinGeckoAPI()
        self.currency_list = self.cg.get_supported_vs_currencies()

    def get_data(self, selected_fiat):
        self.coin_data = self.cg.get_coins_markets(vs_currency=selected_fiat, per_page=None)

    def send_email(self, email_provider, recipient_email, email_password, selected_coin, selected_fiat):
        coin_data = [coin for coin in self.coin_data if coin['id'] == selected_coin][0]

        c_name = coin_data['name']
        c_current_price = coin_data['current_price']
        c_high_24h = coin_data['high_24h']
        c_low_24h = coin_data['low_24h']
        c_price_change_24h = coin_data['price_change_24h']

        message = f"Daily Price Update for {c_name} ({selected_fiat.upper()})\n\n"
        message += f"Current Price: {c_current_price:.2f} {selected_fiat.upper()}\n"
        message += f"24h High: {c_high_24h:.2f} {selected_fiat.upper()}\n"
        message += f"24h Low: {c_low_24h:.2f} {selected_fiat.upper()}\n"
        message += f"24h Price Change: {c_price_change_24h:.2f} {selected_fiat.upper()}\n"

        if email_provider.lower() == "gmail":
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
        elif email_provider.lower() == "outlook":
            smtp_server = "smtp.office365.com"
            smtp_port = 587
        elif email_provider.lower() == "yahoo":
            smtp_server = "smtp.mail.yahoo.com"
            smtp_port = 587
        else:
            print("Invalid email provider. Please choose from Gmail, Outlook, or Yahoo.")
            return

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(recipient_email, email_password)
            msg = MIMEText(message)
            msg['Subject'] = f"Daily Price Update for {c_name}"
            msg['From'] = recipient_email
            msg['To'] = recipient_email
            server.send_message(msg)
            print(f"Email sent to {recipient_email}")
        except Exception as e:
            print(f"Error sending email: {e}")
        finally:
            server.quit()

    def run(self):
        """
        Run the CoinLister program.
        """
        m = menu3.Menu(True)
        menu_1 = m.menu("Choose a fiat:", self.currency_list)
        selected_fiat = self.currency_list[menu_1 - 1]
        m.success("You selected: " + selected_fiat)

        self.get_data(selected_fiat)

        options = ["Top 100 by Market cap", "All"]
        menu_2 = m.menu("Choose an option:", options)
        selected_option = options[menu_2 - 1]
        m.success("You selected: " + selected_option)

        if selected_option == options[0]:
            coin_names = [coin['name'] for coin in self.coin_data[:100]]
        else:
            coin_names = [coin['name'] for coin in self.coin_data]

        menu_3 = m.menu("Choose a cryptocurrency:", coin_names)
        selected_coin = self.coin_data[menu_3 - 1]['id']
        print(f"You selected: {selected_coin}")

        email_provider = input("Enter your email provider (Gmail, Outlook, or Yahoo): ").lower()
        recipient_email = input("Enter your email address: ")
        email_password = getpass.getpass("Enter your email password: ")
        send_time = input("Enter the time to send the email (HH:MM 24-hour format): ")

        schedule.every().day.at(send_time).do(self.send_email, email_provider, recipient_email, email_password, selected_coin, selected_fiat)

        print(f"Daily price update for {selected_coin.upper()} will be sent to {recipient_email} at {send_time}")

        while True:
            schedule.run_pending()
            time.sleep(60)

# Example usage
coin_lister = CoinLister()
coin_lister.run()