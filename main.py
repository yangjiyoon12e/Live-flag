import fastf1
import requests
import time
import os

# GitHub Secrets에서 가져오기
TOPIC = os.getenv("NTFY_TOPIC")
NTFY_URL = f"https://ntfy.sh/{TOPIC}"

def send_ntfy(message):
    requests.post(NTFY_URL, data=message.encode('utf-8'), headers={"Title": "🏁 F1 Race Control"})

def monitor():
    # 1. 2024년 전체 일정 가져오기
    schedule = fastf1.get_event_schedule(2024)
    
    # 2. 현재 시간 기준으로 가장 가까운 세션 찾기
    now = time.time()
    # 현재 시간보다 앞서 있는(진행 중이거나 곧 시작할) 세션 검색
    current_session = None
    for _, event in schedule.iterrows():
        # 각 이벤트의 세션들 확인
        for i in range(1, 6):
            try:
                session = fastf1.get_session(2024, event['EventName'], i)
                if session.date_start.timestamp() - 3600 < now < session.date_end.timestamp() + 3600:
                    current_session = session
                    break
            except:
                continue
    
    if not current_session:
        print("현재 진행 중인 세션이 없습니다.")
        return

    # 3. 데이터 로드
    current_session.load(telemetry=False, laps=False, weather=False)
    messages = current_session.race_control_messages
    
    if not messages.empty:
        # 최근 메시지 하나만 알림 (테스트용)
        latest_msg = messages.iloc[-1]['Message']
        print(f"최신 메시지: {latest_msg}")
        send_ntfy(latest_msg)

if __name__ == "__main__":
    monitor()
