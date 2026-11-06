# 뉴스레이다 · 법조팀판

CBS 법조팀(팀장 장성주 — 송영훈·이원석·나채영·주보배·김지은)용 보고 준비 페이지. 원본 [tolibre/news-monitor](https://github.com/tolibre/news-monitor)에서 설정만 바꿔 만든 판이다(2026-11-07).
같은 묶음: 검찰반판 [newsradar-prosecution](https://github.com/tolibre/newsradar-prosecution)(송영훈).

- 페이지: https://tolibre.github.io/newsradar-legal/ (→ `/live/`)
- 섹션(기울임 = 제목 판정 전용, 네이버 검색 안 함) + 맨 끝 'CBS 법조팀'(팀원 여섯 명 노컷 기사, 보고 양식 `<기처리>`에 `제목(쓴 기자)`)

| 섹션 | 검색어 |
|---|---|
| 법무부 | 법무부 · *법무장관* · 검찰인권존중미래위원회 · *검찰미래위* |
| 공소청 | 공소청 · 서울광역공소청 · 서울중앙지방공소청 · *중앙공소청* · *검찰총장* |
| 중수청 | 중대범죄수사청 · 중수청 |
| 공수처 | 고위공직자범죄수사처 · 공수처 |
| 공소취소 | 공소취소 · *공소 취소* |
| 대법원 | 대법원 · 법원행정처 |
| 서울법원 | 서울고등법원 · 서울고법 · 서울중앙지방법원 · 서울중앙지법 · *중앙지법* · 서울행정법원 · *행정법원* · 서울가정법원 · *가정법원* · 서울회생법원 · *회생법원* |
| 헌재 | 헌법재판소 · 헌재 |
| 법조단체 | 대한변호사협회 · 변협 · 법률구조공단 · 민주사회를위한변호사모임 · 민변 |
| 내란특검 | 내란 특검 · *내란특검* |
| 종합특검 | 종합 특검 · *종합특검* |
| 김건희특검 | 김건희 특검 · *김건희특검* |
| 순직해병특검 | 순직해병 특검 · *순직해병특검* · *해병 특검* · *해병특검* |
| 선관위특검 | 선관위 특검 · *선관위특검* |
| 조작기소특검 | 조작기소 특검 · *조작기소특검* · *조작 기소 특검* |

- 휴일 특근 없음(팀 전원 출입처가 본 섹션). 특검·공소취소 섹션끼리 걸친 사안은 기사가 많은 섹션으로 모은다(원본 0-33). 지역 기사 접기·노컷 기출고·국회 일정 띠(법사위·본회의)·특근 없는 휴일 시간표 등은 원본과 같다.
- DB 보관 45일, 저장키 `nm-legal-*`, 기기 연동·텔레그램 없음.

## 코드를 직접 고치지 말 것

`news_monitor.py`·`render_page.py`·`merge_db.py`·`retitle.py`는 **`tools/make_variant.py`가 원본에서 생성**한다.

```
git clone --depth 1 https://github.com/tolibre/news-monitor /tmp/nm
python tools/make_variant.py /tmp/nm .
```

검색어·섹션·오탐 규칙·기관장 이름은 **`tools/legal_team.py` 한 곳**에서 관리한다 — 법조팀판(`newsradar-legal`)·검찰반판(`newsradar-prosecution`)에 같은 사본이 있으니 둘 다 같게 고칠 것.
`live_links.json`(국회 일정 띠 — 법사위 전부 + 본회의)·`docs/index.html`·yml은 생성기 밖 파일.

## 운영 (cron-job.org → workflow_dispatch)

URL `https://api.github.com/repos/tolibre/newsradar-legal/actions/workflows/newsradar-legal.yml/dispatches`, POST, 헤더는 원본 잡과 같음(PAT `news-monitor-cron`에 이 저장소 추가), Asia/Seoul.

| 잡 | 스케줄 | body |
|---|---|---|
| legal-check | `0 * * * *` | `{"ref":"main","inputs":{"mode":"check"}}` |
| legal-precut | `25 8,13 * * 1-5` | 위와 같음 |
| legal-digest | `0 6 * * *` | `{"ref":"main","inputs":{"mode":"digest"}}` |
| legal-retitle | `15 */2 * * *` | `{"ref":"main","inputs":{"mode":"retitle","apply":"1","limit":"100"}}` |

Secrets: `NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET`(원본과 같은 값). Pages: main / docs.
