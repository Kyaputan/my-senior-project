try:
    import requests
    from dotenv import load_dotenv
    import os
    import logging
except Exception as e:
    print(f"An error occurred: {e}")

load_dotenv()
API_KEY = os.getenv("API_KEY")
print(API_KEY)


logging.basicConfig(
    filename="logs/TestAPIlogs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8", 
)

def send_line_notification(message , TOKEN = API_KEY):
    url_line = "https://notify-api.line.me/api/notify"
    
    LINE_HEADERS = {"Authorization": "Bearer " + TOKEN}
    session = requests.Session()
    START = session.post(url_line, headers=LINE_HEADERS, data={"message": message})
    if START.status_code == 200:
        logging.info(f"ส่งข้อความสำเร็จ: {START.text}")
    else:
        logging.error(f"เกิดข้อผิดพลาด: {START.status_code}, {START.text}")

if __name__ == "__main__":
    try:
        send_line_notification("Hello, World!")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        





