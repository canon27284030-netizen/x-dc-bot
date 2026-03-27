import os, requests, json, time
from ntscraper import Nitter

# Secrets에서 설정값 가져오기
DC_ID = os.environ.get('DC_ID')
DC_PW = os.environ.get('DC_PW')
DC_GALL = os.environ.get('TARGET_GALL')

# --- [감시할 X 계정 목록] ---
TARGET_USERS = [
    'DDDDragon_', 'Mang_nae_', 'damyui_', 'honeychurros1', 
    'AyaUke_V', 'projecti_kr', 'ORIGOGI0011', 'HaSiyo_Projecti', 
    'Siho_Projecti', 'POx4_Projecti', 'Rose_Projecti', 
    'Mone_Projecti', 'Mu_nanS2'
]
# --------------------------

DB_FILE = "last_tweets.json"
scraper = Nitter()
session = requests.Session()

def login_dc():
    # 디시인사이드 로그인
    login_url = "https://www.dcinside.com/auth/login"
    data = {'user_id': DC_ID, 'pw': DC_PW, 's_url': 'https://www.dcinside.com'}
    session.post(login_url, data=data)

def post_to_dc(user, text, link):
    write_url = "https://gall.dcinside.com/board/forms/article_submit"
    title = f"[{user}] X 새 게시글 알림"
    # 내용이 너무 길 경우를 대비해 본문 구성
    content = f"@{user} 계정에 새로운 트윗이 올라왔습니다.\n\n내용:\n{text}\n\n링크: {link}"
    payload = {
        'id': DC_GALL,
        'subject': title,
        'memo': content,
        'mode': 'write'
    }
    session.post(write_url, data=payload)

# 중복 방지 파일 로드
history = {}
if os.path.exists(DB_FILE):
    try:
        with open(DB_FILE, "r") as f:
            history = json.load(f)
    except:
        history = {}

login_dc()

for user in TARGET_USERS:
    try:
        print(f"@{user} 확인 중...")
        # 최신 트윗 1개 가져오기
        tweets = scraper.get_posts(user, mode='user', number=1)
        
        if tweets['tweets']:
            tweet = tweets['tweets'][0]
            link = tweet['link']
            
            # 이전에 올린 링크와 다를 경우에만 게시
            if True: # history.get(user) != link:
                print(f"새 글 발견! @{user}")
                post_to_dc(user, tweet['text'], link)
                history[user] = link
                # 디시인사이드 도배 방지를 위해 계정당 3초씩 대기
                time.sleep(3)
    except Exception as e:
        print(f"@{user} 체크 중 오류 발생: {e}")

# 최신 상태 저장
with open(DB_FILE, "w") as f:
    json.dump(history, f)
