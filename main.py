import os, requests, json, time
from ntscraper import Nitter

# Secrets 설정
DC_ID = os.environ.get('DC_ID')
DC_PW = os.environ.get('DC_PW')
DC_GALL = os.environ.get('TARGET_GALL')

TARGET_USERS = [
    'DDDDragon_', 'Mang_nae_', 'damyui_', 'honeychurros1', 
    'AyaUke_V', 'projecti_kr', 'ORIGOGI0011', 'HaSiyo_Projecti', 
    'Siho_Projecti', 'POx4_Projecti', 'Rose_Projecti', 
    'Mone_Projecti', 'Mu_nanS2'
]

DB_FILE = "last_tweets.json"
scraper = Nitter()
session = requests.Session()

def login_dc():
    login_url = "https://www.dcinside.com/auth/login"
    data = {'user_id': DC_ID, 'pw': DC_PW, 's_url': 'https://www.dcinside.com'}
    session.post(login_url, data=data)

def post_to_dc(user, text, link):
    write_url = "https://gall.dcinside.com/board/forms/article_submit"
    title = f"[{user}] X 새 게시글"
    content = f"@{user} 새 트윗\n\n내용:\n{text}\n\n링크: {link}"
    payload = {'id': DC_GALL, 'subject': title, 'memo': content, 'mode': 'write'}
    session.post(write_url, data=payload)

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
        # 데이터를 가져오지 못할 경우를 대비해 인스턴스를 무작위로 선택
        tweets = scraper.get_tweets(user, mode='user', number=1)
        
        if tweets and 'tweets' in tweets and len(tweets['tweets']) > 0:
            tweet = tweets['tweets'][0]
            link = tweet['link']
            
            # 이전에 올린 링크와 다를 경우에만 게시
            if history.get(user) != link:
                print(f"새 글 발견! @{user}")
                post_to_dc(user, tweet['text'], link)
                history[user] = link
                time.sleep(3)
        else:
            print(f"@{user}: 현재 X 서버 응답이 없습니다. 잠시 후 다시 시도합니다.")
            
    except Exception as e:
        print(f"@{user} 처리 중 건너뜀: 서버 연결 불안정")

with open(DB_FILE, "w") as f:
    json.dump(history, f)
