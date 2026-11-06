
# ==================== 법조팀 판: 국회팀판 방식의 매체 가점·주요 매체·접기 (0-95b, 2026-11-07) ====================
# tools/make_variant.py가 이 파일 내용을 news_monitor.py 맨 아래(main 바로 앞)에 넣는다(국회팀판 tools/asm_fold.py와 같은 방식 —
# 원본 함수는 그대로 두고 전역 이름 _attach_weak·build_live_data를 감싼다). 두 법조팀 저장소에 같은 사본.
#
# 사용자 결정(11/7 02:33): "가점 부여는 국회팀 부여 방식을 따르고, 주요매체 구분이나 접기도 국회팀 쪽과 매커니즘을 비슷하게.
#   경제지 비중은 줄이되 법조 전문매체도 모니터 대상에 포함."
#  ① 주요 매체 = 국회팀판 목록(통신 3 + 종합일간지 10 + 방송 9 + 헤럴드경제·데일리안·오마이뉴스·노컷뉴스·내일신문) + **법률신문**.
#     경제지(매경·한경·머투·서경·이데일리·아경·파뉴)는 주요 매체가 아니다 → 경제지만 받은 묶음은 접힌다.
#  ② 한 매체만 쓴 묶음은 접는다(국회팀 0-90). 예외: 그 매체가 종합일간지 10곳 또는 법률신문(국회팀 0-91 + 법조 전문지 1위).
#  ③ [단독]은 접지 않는다. 접기는 원본 '관련 약함' 장치 — 묶음 기사 전부가 wk일 때만 섹션 끝 접힌 줄로.
#  지역 접기는 원본 규칙(LIVE_REGION_FOLD)·'제목에 이름 없음'(legal_team.FOLD_GROUPS)이 그대로 함께 돈다(국회팀판의 시·도당 규칙은 정당용이라 안 씀).

LEGAL_MAJOR_MEDIA = {
    "연합뉴스", "뉴시스", "뉴스1",
    "조선일보", "중앙일보", "동아일보", "한겨레", "경향신문", "한국일보", "서울신문", "국민일보", "세계일보", "문화일보",
    "KBS", "KBS 뉴스", "MBC", "MBC 뉴스", "SBS", "SBS 뉴스", "YTN", "연합뉴스TV", "JTBC", "TV조선", "채널A", "MBN",
    "헤럴드경제", "데일리안", "오마이뉴스", "노컷뉴스", "CBS노컷뉴스", "내일신문",
    "법률신문",
}
LEGAL_MAJOR_MEDIA |= {short_media_name(x) for x in LEGAL_MAJOR_MEDIA}
LEGAL_SOLO_OK = {"조선일보", "중앙일보", "동아일보", "한겨레", "경향신문", "한국일보", "서울신문", "국민일보", "세계일보", "문화일보",
                 "법률신문"}
LEGAL_SOLO_OK |= {short_media_name(x) for x in LEGAL_SOLO_OK}

LEGAL_WL_DESC = ("한 매체만 쓴 묶음(종합일간지 10곳·법률신문 기사는 펼쳐 둠), 주요 매체(통신 3·종합지 10·방송 9·헤럴드경제·데일리안·오마이뉴스·"
                 "노컷뉴스·내일신문·법률신문)가 한 곳도 받지 않은 묶음, 지역 사안 묶음을 섹션 끝에 접어 둡니다. "
                 "법무부·대법원·서울법원·헌재·법조단체는 제목에 기관 이름(법원 기사는 '법원·法·재판부·선고' 같은 말 포함)이 없는 묶음도 접습니다. "
                 "[단독]은 접지 않고, 건수에는 포함하며, 검색·‘선택’ 보기에서는 펼쳐 보입니다.")


def legal_fold_reason(title, source):
    """주요 매체 밖이면 '비주요', 아니면 ''. [단독]은 늘 ''."""
    if priority_mark(title) == "🔥":
        return ""
    if (source or "").strip() not in LEGAL_MAJOR_MEDIA:
        return "비주요"
    return ""


_legal_orig_attach_weak = _attach_weak


def _attach_weak(groups):
    n = _legal_orig_attach_weak(groups)
    for g in groups:
        for clu in g["clusters"]:
            outs = {(it.get("s") or "").strip() for it in clu}
            one = (len(outs) <= 1 and not any(priority_mark(it.get("t") or "") == "🔥" for it in clu)
                   and not (outs & LEGAL_SOLO_OK))
            for it in clu:
                if not it.get("wk") and (one or legal_fold_reason(it.get("t") or "", it.get("s") or "")):
                    it["wk"] = 1
                    n += 1
    return n


_legal_orig_build_live_data = build_live_data


def build_live_data(conn, now):
    out = _legal_orig_build_live_data(conn, now)
    wl = out.setdefault("wl", {})
    for g in list(GROUP_ORDER) + list(DUTY_ONLY_GROUPS):
        wl[g] = {"label": "한 매체·비주요·지역", "desc": LEGAL_WL_DESC}
    return out

