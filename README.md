# 🤖 GitHub Trend Bot (Discord Notification)

매일 지정된 시간에 **GitHub Trending(인기 리포지토리)** 정보를 수집하여 **Discord**로 알림을 보내주는 자동화 봇입니다.
5가지 주요 언어(Python, Java, JavaScript, TypeScript, Kotlin)의 일간 트렌드를 분석하고, 설명을 한국어로 번역하여 각 언어별 전용 채널로 전송합니다.

## ✨ 주요 기능 (Key Features)

* **📅 자동화된 스케줄:** GitHub Actions를 이용해 매일 한국 시간 낮 12:00 (UTC 03:00)에 자동 실행됩니다.
* **🌍 다국어 지원:** 5개 프로그래밍 언어의 트렌드를 각각 수집합니다.
* **💬 자동 번역:** 리포지토리의 영문 설명을 `deep-translator`를 사용해 한국어로 번역합니다.
* **📢 채널별 분리 전송:** 언어별로 서로 다른 Discord Webhook을 사용하여, 관련된 채널에만 알림을 보냅니다.
* **🔒 보안:** Webhook URL은 GitHub Secrets로 안전하게 관리됩니다.

## 🛠 기술 스택 (Tech Stack)

* **Language:** Python 3.9
* **Libraries:** `requests`, `beautifulsoup4`, `deep-translator`
* **Infrastructure:** GitHub Actions (Cron Job)
* **Notification:** Discord Webhook 

## 📂 프로젝트 구조 (Structure)

```text
github-trend-bot/
├── .github/
│   └── workflows/
│       └── daily_trend.yml    # GitHub Actions 스케줄 설정
├── src/
│   ├── __init__.py
│   └── main.py                # 크롤링 및 디스코드 전송 로직
├── .gitignore
├── README.md
└── requirements.txt           # 의존성 패키지 목록


