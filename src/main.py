import os
import time
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from datetime import datetime

# --- 설정: 언어별 웹후크 매핑 ---
# 환경 변수에서 각각의 URL을 가져와 딕셔너리로 묶습니다.
WEBHOOK_MAP = {
    "python": os.environ.get("WEBHOOK_PYTHON"),
    "javascript": os.environ.get("WEBHOOK_JAVASCRIPT"),
    "typescript": os.environ.get("WEBHOOK_TYPESCRIPT"),
    "java": os.environ.get("WEBHOOK_JAVA"),
    "kotlin": os.environ.get("WEBHOOK_KOTLIN")
}

def get_github_trends(language):
    """(이전과 동일) 특정 언어의 GitHub Trending을 크롤링합니다."""
    url = f"https://github.com/trending/{language}?since=daily"
    print(f"[{language}] 데이터 수집 중...")
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200: return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        repos = []
        
        for item in soup.select('article.Box-row')[:5]:
            try:
                h1 = item.select_one('h2.h3 a')
                name = h1.text.strip().replace('\n', '').replace(' ', '')
                link = f"https://github.com{h1['href']}"
                
                stats = item.select('a.Link--muted')
                stars = stats[0].text.strip() if len(stats) > 0 else "0"
                forks = stats[1].text.strip() if len(stats) > 1 else "0"
                
                desc_tag = item.select_one('p.col-9')
                description_en = desc_tag.text.strip() if desc_tag else "No description."
                
                try:
                    description_ko = GoogleTranslator(source='auto', target='ko').translate(description_en)
                except:
                    description_ko = description_en

                repos.append({
                    'name': name, 'link': link, 'stars': stars, 'forks': forks, 'desc': description_ko
                })
            except: continue
        return repos
    except Exception as e:
        print(f"[{language}] 에러: {e}")
        return []

def send_discord_message(repos, language):
    """언어에 맞는 웹후크 URL을 찾아 메시지를 전송합니다."""
    # 1. 현재 언어에 해당하는 웹후크 URL 찾기
    webhook_url = WEBHOOK_MAP.get(language)
    
    if not webhook_url:
        print(f"⚠️ [{language}] 전송 실패: 해당 언어의 웹후크 URL이 설정되지 않았습니다.")
        return

    today = datetime.now().strftime('%Y-%m-%d')
    emoji_map = {"python": "🐍", "javascript": "🟨", "typescript": "📘", "java": "☕", "kotlin": "🟣"}
    
    content = f"## {emoji_map.get(language, '🌐')} 트렌드: **{language.upper()}** ({today})\n"
    for idx, repo in enumerate(repos, 1):
        content += f"**{idx}. {repo['name']}** (⭐️`{repo['stars']}` | 🍴`{repo['forks']}`)\n"
        content += f"> {repo['desc']}\n"
        content += f"- <{repo['link']}>\n\n"
    
    # 2. 찾은 URL로 전송
    requests.post(webhook_url, json={"content": content})
    print(f"✅ [{language}] 전송 완료")
    time.sleep(1)

if __name__ == "__main__":
    print("=== GitHub Trend Bot 시작 ===")
    
    # WEBHOOK_MAP에 정의된 키(언어)들만 순회합니다.
    for lang in WEBHOOK_MAP.keys():
        trends = get_github_trends(lang)
        if trends:
            send_discord_message(trends, lang)
            
    print("=== 모든 작업 완료 ===")