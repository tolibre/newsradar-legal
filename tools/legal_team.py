# -*- coding: utf-8 -*-
"""법조팀 출입처 묶음 — 뉴스레이다 법조팀 변형판 공용 설정(0-95, 2026-11-07).

사용자 결정(11/7 00:5x): 판 두 개 —
  ① 법조팀판 `tolibre/newsradar-legal` — 팀원 여섯 명 출입처 전부가 본 섹션, 휴일 특근 없음.
     팀원: 장성주(팀장)·송영훈·이원석(중수청)·나채영(공소청)·주보배·김지은(법원).
  ② 송영훈판(검찰반장) `tolibre/newsradar-prosecution` — 공소청·중수청·공수처·공소취소·특검이 본 섹션,
     휴일 특근을 켜면 법조팀 나머지(법무부·법원·헌재·법조단체)가 잡힌다.
특검은 특검마다 섹션(사용자), 법원은 대법원 / 서울 법원 둘(사용자), '조작기소 특검'은 두 판 모두 추가(사용자 —
기존 판 DB 제목 '특검' 3,208건 중 약 2,100건이 조작기소 특검이었다).

**이 파일은 법조팀 저장소마다 같은 사본이 있다**(newsradar-legal·newsradar-prosecution). 하나를 고치면 둘 다 같게 바꾸고
두 생성기를 다시 돌릴 것. 그룹 이름 = 각 판의 섹션 이름(송영훈판 당직 그룹 = 이 묶음 중 자기 섹션이 아닌 것).
"""

# (그룹, [(검색어, 네이버 검색 여부), ...]) — 순서 = 섹션 순서(사용자 11/7 목록 순서).
# 검색 여부 False = 제목 판정 전용(KEYWORD_MAX_PAGES 0). 구글 뉴스 RSS는 이 말로도 검색한다(0-70 교훈).
# 사용자 목록의 말은 전부 검색한다. 약칭·붙여 쓴 꼴은 제목 판정용으로 더했다(본문엔 정식 명칭이 함께 나온다).
TEAM = [
    ("법무부", [("법무부", True), ("법무장관", False),
               ("검찰인권존중미래위원회", True), ("검찰미래위", False)]),
    # '공소청'은 서울광역공소청·서울중앙지방공소청·'중앙공소청'(언론 약칭)의 부분 문자열이라 제목 판정은 한 말로 다 걸린다.
    # 공소청 수장 직함은 여전히 '검찰총장'(공소청법) — 제목 판정 전용으로 더함.
    ("공소청", [("공소청", True), ("서울광역공소청", True), ("서울중앙지방공소청", True),
               ("중앙공소청", False), ("검찰총장", False)]),
    ("중수청", [("중대범죄수사청", True), ("중수청", True)]),
    ("공수처", [("고위공직자범죄수사처", True), ("공수처", True)]),
    ("공소취소", [("공소취소", True), ("공소 취소", False)]),
    ("대법원", [("대법원", True), ("법원행정처", True)]),
    ("서울법원", [("서울고등법원", True), ("서울고법", True),
                ("서울중앙지방법원", True), ("서울중앙지법", True), ("중앙지법", False),
                ("서울행정법원", True), ("행정법원", False),
                ("서울가정법원", True), ("가정법원", False),
                ("서울회생법원", True), ("회생법원", False)]),
    ("헌재", [("헌법재판소", True), ("헌재", True)]),
    ("법조단체", [("대한변호사협회", True), ("변협", True), ("법률구조공단", True),
                ("민주사회를위한변호사모임", True), ("민변", True)]),
    ("내란특검", [("내란 특검", True), ("내란특검", False)]),
    ("종합특검", [("종합 특검", True), ("종합특검", False)]),
    ("김건희특검", [("김건희 특검", True), ("김건희특검", False)]),
    # '해병 특검'은 '순직해병 특검'·'채해병 특검'을 함께 품는다(언론은 둘 다 쓴다).
    ("순직해병특검", [("순직해병 특검", True), ("순직해병특검", False), ("해병 특검", False), ("해병특검", False)]),
    ("선관위특검", [("선관위 특검", True), ("선관위특검", False)]),
    ("조작기소특검", [("조작기소 특검", True), ("조작기소특검", False), ("조작 기소 특검", False)]),
]
SONG_GROUPS = ["공소청", "중수청", "공수처", "공소취소",
               "내란특검", "종합특검", "김건희특검", "순직해병특검", "선관위특검", "조작기소특검"]
ALL_GROUPS = [g for g, _ in TEAM]
SPEC = dict(TEAM)

# 같은 사안이 특검·공소취소 섹션에 걸치면 기사가 가장 많은 섹션으로 모은다(원본 0-33 — 국회판에서 쓰는 기능).
# 조작기소 특검은 공소취소 권한 논쟁과 한 사안이고, 종합특검·내란특검은 수사 대상이 겹친다.
STORY_MERGE = ["공소취소", "내란특검", "종합특검", "김건희특검", "순직해병특검", "선관위특검", "조작기소특검"]

# 단어 일부 오매칭 예방 — 제목에서 이 표현을 지운 뒤에도 검색어가 남아야 매칭.
ANTI = {
    # 서울 아닌 가정법원·회생법원(부산가정법원·수원회생법원 등) — '서울법원' 섹션은 서울 법원만.
    "가정법원": [r"(?:부산|대구|대전|광주|인천|수원|울산|창원|전주|춘천|제주|청주|의정부)\s?가정법원"],
    "회생법원": [r"(?:부산|수원|대구|대전|광주)\s?회생법원"],
    # '시민변호사'·'국민변호인단' 같은 말 속의 '민변' — 앞뒤가 모두 한글이면 다른 말.
    "민변": [r"[가-힣]민변(?=[가-힣])"],
    # '검찰총장'은 옛 기사 회고('윤석열 전 검찰총장')가 많다 — '전 검찰총장'·'前 검찰총장'은 판정에서 뺀다.
    "검찰총장": [r"(?:전|前)\s?검찰총장"],
}

# 사안어(기관명이 아님) — 클러스터링 '출입처명 토큰'에서 뺀다(원본 0-28 누리호와 같은 이유).
TOPIC_WORDS = ["공소취소"]

# 기관장 이름 씨앗(0-38 — 주체 출입처 판정, DB 학습분이 우선). 2026-11-07 웹 확인:
# 법무부 장관 공석·이진수 차관(11/6 후보자 이용철 방사청장 지명), 박철우 서울중앙지방공소청장, 김지용 중수청장, 오동운 공수처장, 조희대 대법원장,
# 김상환 헌재소장, 특검 조은석(내란)·민중기(김건희)·이명현(순직해병)·권창영(2차 종합)·이태한(선관위).
# 조작기소 특검은 아직 법 통과 전(11/6 본회의 상정). 인사가 바뀌면 고칠 것.
SEED = {"이진수": "법무부", "이용철": "법무부", "박철우": "공소청", "김지용": "중수청", "오동운": "공수처",
        "조희대": "대법원", "김상환": "헌재",
        "조은석": "내란특검", "권창영": "종합특검", "민중기": "김건희특검", "이명현": "순직해병특검", "이태한": "선관위특검"}

# 국회 일정 띠(원본 0-82) — 두 판 모두 법사위 전부 + 본회의. live_links.json(생성기 밖 파일)에 넣는다.
ASSEMBLY = {"label": "국회 일정", "days": 14, "plenary": True,
            "committees": [{"name": "법제사법위원회", "short": "법사위", "exclude": []}]}

KEYWORDS_ALL = [k for _, kws in TEAM for k, _s in kws]
NO_SEARCH = [k for _, kws in TEAM for k, s in kws if not s]
GROUP_OF = {k: g for g, kws in TEAM for k, _s in kws}


def keywords_for(groups):
    return [k for g in groups for k, _s in SPEC[g]]


def duty_only(own_groups):
    return [g for g in ALL_GROUPS if g not in own_groups]


def duty_keywords_block():
    body = "".join(f"    # {g}\n    " + ", ".join(f'"{k}"' for k, _ in kws) + ",\n" for g, kws in TEAM)
    return ("DUTY_KEYWORDS = [\n"
            "    # 법조팀 묶음(tools/legal_team.py — 생성기가 원본 경제정책팀 묶음 자리에 넣는다)\n"
            + body + "]\n")


def duty_groups_block():
    body = "".join("    " + ", ".join(f'"{k}": "{g}"' for k, _ in kws) + ",\n" for g, kws in TEAM)
    return "DUTY_KEYWORD_GROUPS = {\n" + body + "}\n"


def anti_lines():
    return "".join(f'    "{k}": ' + "[" + ", ".join(f'r"{p}"' for p in pats) + "],   # 법조팀(legal_team.py)\n"
                   for k, pats in ANTI.items())


def max_pages_block():
    return ('KEYWORD_MAX_PAGES = {\n    "CBS": 1,\n    '
            + ", ".join(f'"{k}": 0' for k in NO_SEARCH)
            + ",   # 법조팀(legal_team.py) — 제목 판정 전용\n}\n")


def topic_line():
    return "CLUSTER_TOPIC_KEYWORDS = {" + ", ".join(f'"{w}"' for w in ["누리호"] + TOPIC_WORDS) + "}   # 법조팀 사안어 추가(legal_team.py)\n"


# ---- 휴일 특근(당직) 섹션 '제목에 이름 없음' 접기(원본 0-69 LIVE_FOLD_KEEP, 사회정책팀 0-72 방식) ----
# 송영훈판의 당직 섹션(법무부·대법원·서울법원·헌재·법조단체)만 — 제목에 그 기관 이름(기관장 직함 포함)이 없는 묶음을 접는다.
# 자기 섹션에는 안 건다. [단독]은 안 접는다.
DUTY_FOLD_EXTRA = {
    "법무부": ["법무차관", "이진수", "이용철"],
    # 첫 실행 실측(11/7 02:08): 법원 기사는 제목에 법원 이름 대신 '법원'·'法'만 쓰는 판결 기사가 많다('[속보] 법원, 쿠팡 과징금 효력정지' 49건·
    # '법관대표회의 조기 소집' 33건이 접혔다) → 법원·재판 일반어도 남긴다. 접히는 건 SK 지분·삼성바이오 파업 같은 본문 스침 기사.
    "대법원": ["대법원장", "대법관", "조희대", "사법부", "법관", "법원", "法", "상고", "확정"],
    "서울법원": ["서울남부지법", "서울동부지법", "서울서부지법", "서울북부지법",
                 "법원", "法", "재판부", "1심", "2심", "항소심", "징역", "무죄", "선고", "구속영장", "영장"],
    "헌재": ["헌법재판관", "헌법소원", "재판소원", "김상환"],
    "법조단체": ["변호사협회", "변호사회"],
}
FOLD_GROUPS = ["법무부", "대법원", "서울법원", "헌재", "법조단체"]
# 사용자(11/7 02:18) "접기 걸자" — 법조팀판 본 섹션에도 같은 규칙(송영훈판은 이 다섯이 휴일 특근 섹션).
DUTY_FOLD_DESC = ("법무부·대법원·서울법원·헌재·법조단체 섹션은 제목에 기관 이름(법원 기사는 '법원·法·재판부·선고' 같은 말 포함)이 없는 묶음 — "
                  "본문에만 이름이 스친 기사 — 을 섹션 끝에 접어 둡니다. [단독]은 접지 않고, 건수에는 포함합니다.")


def fold_keep(own_groups=None):
    """LIVE_FOLD_KEEP — FOLD_GROUPS 다섯 섹션(본 섹션이든 휴일 특근 섹션이든)."""
    import re as _re
    out = {}
    for g in FOLD_GROUPS:
        words = [k for k, _s in SPEC[g]] + DUTY_FOLD_EXTRA.get(g, [])
        out[g] = {"keep": [], "fold": [], "need": [_re.escape(w) for w in words],
                  "label": "제목에 이름 없음", "desc": DUTY_FOLD_DESC}
    return out

# ---- 매체(0-95b, 사용자 11/7 02:33 "국회팀 방식 가점·주요 매체·접기, 경제지 비중 줄이고 법조 전문매체 포함") ----
# 법조 전문매체 — 첫 실행 DB에서 화이트리스트 밖으로 버려지던 것(11/7 02:08: 법률신문 459·로리더 48·법률방송 44·로이슈 39·법조신문 74·
# 로톡뉴스 18·법률저널 19·리걸타임즈 13·'대한민국 법원' 14건). 표시명은 매체가 쓰는 이름.
LEGAL_MEDIA = {   # 도메인 → 표시명
    "lawtimes.co.kr": "법률신문", "lawtv.kr": "법률방송뉴스", "lawissue.co.kr": "로이슈", "lawleader.co.kr": "로리더",
    "news.koreanbar.or.kr": "법조신문", "legaltimes.co.kr": "리걸타임즈", "lec.co.kr": "법률저널", "lawtalknews.co.kr": "로톡뉴스",
    "naeil.com": "내일신문",   # 석간(국회팀판과 같게 — 원본 화이트리스트에 없다)
}
LEGAL_MEDIA_NAMES = sorted(set(LEGAL_MEDIA.values()) | {"법률방송", "대한민국 법원"})
# '전체' 탭 묶음 가산 — 국회팀판과 같은 값(주요 일간지·종편·보도PP·통신 +1.5, 09:00 보고 조간 종합지 +3, 14:00 보고 석간 셋 +3).
# 경제지는 넣지 않는다. 법조 전문지도 가점은 없다(접기 예외만 — legal_fold.py).
DAILY_AM = ["조선일보", "중앙일보", "동아일보", "한국일보", "경향신문", "한겨레", "국민일보", "서울신문", "세계일보"]
DAILY_PM = ["문화일보", "내일신문", "헤럴드경제"]
BROADCAST = ["TV조선", "JTBC", "채널A", "MBN", "YTN", "연합뉴스TV"]
WIRE = ["연합뉴스", "뉴시스", "뉴스1"]
BOOST_BASE, BOOST_SLOT = 1.5, 3.0


def _set_lit(names):
    return "{" + ", ".join(repr(x) for x in sorted(set(names))) + "}"


NEW_BOOST = ("LIVE_MEDIA_BOOST = {\n"
             f'    "*": [({_set_lit(DAILY_AM + DAILY_PM + BROADCAST + WIRE)}, {BOOST_BASE})],\n'
             f'    "am": [({_set_lit(DAILY_AM)}, {BOOST_SLOT})],\n'
             f'    "pm": [({_set_lit(DAILY_PM)}, {BOOST_SLOT})],\n'
             "}   # 법조팀(legal_team.py) — 국회팀판과 같은 값\n")


def media_replacements(NM, fold_src):
    return [
        (NM, 'LIVE_MEDIA_BOOST = {"*": [(LIVE_MEDIA_MAJOR, 1.0)]}\n', NEW_BOOST, 1, False),
        (NM, "STORE_NON_WHITELIST = True\n",
             "STORE_NON_WHITELIST = True\nMEDIA_DOMAINS.update(" + repr(sorted(LEGAL_MEDIA)) + "); MEDIA_NAMES.update("
             + repr(LEGAL_MEDIA_NAMES) + ")   # 법조팀(legal_team.py) — 법조 전문매체·내일신문\n", 1, False),
        (NM, "def media_name(source):\n",
             "DOMAIN_TO_NAME.update(" + repr(dict(sorted(LEGAL_MEDIA.items()))) + ")   # 법조팀(legal_team.py)\n\ndef media_name(source):\n", 1, False),
        (NM, "# ==================== main ====================\nif __name__ == \"__main__\":\n",
             fold_src + "# ==================== main ====================\nif __name__ == \"__main__\":\n", 1, False),
    ]


def replacements(NM, RP, own_groups):
    """법조팀 생성기 공통 치환(원본 기준 문자열·횟수)."""
    own = list(own_groups)
    groups_line = ("KEYWORD_GROUPS.update(DUTY_KEYWORD_GROUPS)\n"
                   "KEYWORD_GROUPS.update(" + repr({k: GROUP_OF[k] for k in keywords_for(own)}) + ")   # 법조팀(생성기)\n")
    base = ("BASE_KEYWORDS = [\n"
            "    # 뉴스레이다 법조팀 변형판(tools/make_variant.py가 tools/legal_team.py로 생성 — 직접 고치지 말 것).\n"
            "    # 순서 = 섹션 판정 순서(제목에 둘 이상 걸리면 앞 그룹). 제목 판정 전용어는 KEYWORD_MAX_PAGES 0.\n"
            + "".join(f'    "{k}",\n' for k in keywords_for(own)) + "]\n")
    fk = fold_keep(own)
    with open(__file__.replace("legal_team.py", "legal_fold.py"), encoding="utf-8") as f:
        fold_src = f.read()
    return media_replacements(NM, fold_src) + [
        (NM, r"DUTY_KEYWORDS = \[\n(?:.*\n)*?\]\n", duty_keywords_block(), 1, True),
        (NM, r"DUTY_KEYWORD_GROUPS = \{\n(?:.*\n)*?\}\n", duty_groups_block(), 1, True),
        (NM, 'KEYWORD_MAX_PAGES = {\n    "CBS": 1,\n}\n', max_pages_block(), 1, False),
        (NM, 'CLUSTER_TOPIC_KEYWORDS = {"누리호"}\n', topic_line(), 1, False),
        (NM, '    "개인정보위": [],\n', '    "개인정보위": [],\n' + anti_lines(), 1, False),
        (NM, r"EXCLUDE_TERMS = \[\n(?:.*\n)*?\]\n",
             "EXCLUDE_TERMS = []   # 이 판은 '공정위'를 검색하지 않아 공정위 오탐용 제외어가 필요 없다(생성기, 0-46)\n", 1, True),
        (NM, r"BASE_KEYWORDS = \[\n(?:.*\n)*?\]\n", base, 1, True),
        (NM, 'TEMP_KEYWORDS = {\n    "대미투자": "2026-09-23",\n}\n', "TEMP_KEYWORDS = {}\n", 1, False),
        (NM, "KEYWORD_GROUPS.update(DUTY_KEYWORD_GROUPS)\n", groups_line, 1, False),
        (NM, "LIVE_STORY_MERGE_GROUPS = []\n",
             f"LIVE_STORY_MERGE_GROUPS = {[g for g in STORY_MERGE if g in own]!r}   # 법조팀(legal_team.py) — 특검·공소취소 걸친 사안 합치기\n", 1, False),
        (NM, "RETENTION_DAYS = 90 ", "RETENTION_DAYS = 45 ", 1, False),
        (NM, "ACTOR_PEOPLE_SEED = {}\n",
             f"ACTOR_PEOPLE_SEED = { {p: g for p, g in SEED.items() if g in own}!r}   # 법조팀(legal_team.py)\n", 1, False),
    ] + ([(NM, "LIVE_FOLD_KEEP = {}\n", f"LIVE_FOLD_KEEP = {fk!r}   # 법조팀 당직 접기(legal_team.py)\n", 1, False)] if fk else [])
