import fastf1
import requests
import time
import os

# GitHub Secrets에서 토픽 이름을 가져오도록 수정
TOPIC = os.getenv("NTFY_TOPIC")
NTFY_URL = f"https://ntfy.sh/{TOPIC}"

def send_ntfy(message):
    requests.post(NTFY_URL, data=message.encode('utf-8'), headers={"Title": "🏁 F1 Race Control"})

def monitor():
    session = fastf1.get_event_schedule(2024).get_session_by_date(time.time())
    session.load()
    last_msg_id = len(session.race_control_messages)
    
    # 세션 데이터 확인
    session.load(telemetry=False, laps=False, weather=False)
    new_messages = session.race_control_messages
    
    if len(new_messages) > last_msg_id:
        for _, row in new_messages.iloc[last_msg_id:].iterrows():
            send_ntfy(row['Message'])

if __name__ == "__main__":
    monitor()
