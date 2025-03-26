try:
    import requests
    from dotenv import load_dotenv
    import os
except Exception as e:
    print(f"An error occurred: {e}")

load_dotenv()
API_KEY = os.getenv("API_KEY")

def send_line_notification(message , TOKEN = API_KEY):
    url_line = "https://notify-api.line.me/api/notify"
    
    LINE_HEADERS = {"Authorization": "Bearer " + TOKEN}
    session = requests.Session()
    return session.post(url_line, headers=LINE_HEADERS, data={"message": message})

if __name__ == "__main__":
    try:
        send_line_notification("Hello, World!")
    except Exception as e:
        print(f"An error occurred: {e}")




