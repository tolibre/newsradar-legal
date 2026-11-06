#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""뉴스레이다 법조팀판(CBS 법조팀, 팀장 장성주) 생성기 — 0-95(2026-11-07).

원본(tolibre/news-monitor — 김광일 기자 출입처판)의 파일을 그대로 가져와
'출입처·바이라인·브라우저 저장키·보관 기간' 같은 설정만 바꿔 이 저장소에 쓴다.
(행정판 tolibre/newsradar-gov 생성기와 같은 구조. 출입처 묶음은 tools/legal_team.py — 송영훈판과 같은 사본.)

  python tools/make_variant.py <원본 저장소 경로> [<출력 경로, 기본=이 저장소>]

- 치환마다 '원본에서 정확히 몇 번 나와야 하는지'를 적어 두고, 다르면 아무 파일도 쓰지 않고 멈춘다.
- 원본 쪽 파일은 읽기만 한다. 함수는 바꾸지 않는다(설정·문구만).
- live_links.json(국회 일정 띠)·docs/index.html·yml은 생성기 밖 파일(이 저장소에 직접).
"""
import hashlib, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import legal_team as LT

# ---------------------------------------------------------------- 설정값 ---
REPORTER = "장성주"                       # 판 주인(법조팀장). 노컷 author 메타 'CBS노컷뉴스 ○○○ 기자' 가정 — 첫 실행에서 확인
TEAM = ["장성주", "송영훈", "이원석", "나채영", "주보배", "김지은"]   # 사용자 11/7: 장성주(팀장) 송영훈·이원석(중수청) 나채영(공소청) 주보배·김지은(법원)
TEAM_SECTION = "CBS 법조팀"
BEATS_TITLE = "법조팀"
STORE_PREFIX = "nm-legal-"                # 브라우저 저장키 — 다른 판(nm-live-·nm-moef-·nm-asm-·nm-ind-·nm-cc-·nm-wel-·nm-lab-·nm-edu-·nm-gov-·nm-land-·nm-ba-·nm-desk-·nm-pros-)과 달라야 한다
GROUPS = list(LT.ALL_GROUPS)              # 법조팀 전원 출입처가 본 섹션
REPORT_ORDER_JS = "[" + ",".join(f"'{g}'" for g in GROUPS) + "]"
COLORS = ["법무부", "공소청", "대법원", "헌재"]   # 원본 네 출입처 색(공정위·과기정통부·방미통위·우주항공청 자리) — 나머지는 회색
WHO = '<span class="who">CBS 법조팀<span class="whob"> (법원·공소청·특검 등)</span></span>'
TAB_TITLE = "뉴스레이다(법조팀)"

NM = "news_monitor.py"
RP = "render_page.py"

REPLACEMENTS = [
    # ---- 출입처(legal_team.py 공통) ----
    *LT.replacements(NM, RP, GROUPS),
    # 휴일 특근 없음 — 팀 전원 출입처가 이미 본 섹션(사용자 11/7). 당직 그룹이 전부 GROUP_ORDER라 어차피 비지만 명시적으로 끈다.
    (NM, "DUTY_COLLECT = True\n", "DUTY_COLLECT = False   # 법조팀판: 팀 전원 출입처가 본 섹션(생성기)\n", 1, False),
    # ---- 바이라인: 팀 여섯 명(원본 0-32 자리 — 국회팀판과 같은 방식) ----
    (NM, 'BYLINE_NAME = "김광일"', f'BYLINE_NAME = "{REPORTER}"', 1, False),
    (NM, 'BYLINE_SECTION = "김광일 기자"', f'BYLINE_SECTION = "{TEAM_SECTION}"', 1, False),
    (NM, "BYLINE_NAMES = [BYLINE_NAME]\n", f"BYLINE_NAMES = {TEAM!r}   # 법조팀(생성기)\n", 1, False),
    (NM, "BYLINE_TRUST_META = False\n", "BYLINE_TRUST_META = True   # 팀 모드 — 방송 녹취 출연 문구 오탐 방지(국회팀판과 같음)\n", 1, False),

    # ---- render_page.py ----
    (RP, "var REPORT_ORDER = ['방미통위','공정위','과기정통부','우주항공청'];", f"var REPORT_ORDER = {REPORT_ORDER_JS};", 2, False),
    (RP, "출입처 순서(방미통위 → 공정위 → 과기정통부 → 우주청 → 2진)", "출입처 순서(" + " → ".join(GROUPS) + ")", 2, False),
    (RP, "'nm-live-", f"'{STORE_PREFIX}", 6, False),
    (RP, '[data-g="공정위"], [data-b="공정위"]', f'[data-g="{COLORS[0]}"], [data-b="{COLORS[0]}"]', 1, False),
    (RP, '[data-g="과기정통부"], [data-b="과기정통부"]', f'[data-g="{COLORS[1]}"], [data-b="{COLORS[1]}"]', 1, False),
    (RP, '[data-g="방미통위"], [data-b="방미통위"]', f'[data-g="{COLORS[2]}"], [data-b="{COLORS[2]}"]', 1, False),
    (RP, '[data-g="우주항공청"], [data-b="우주항공청"]', f'[data-g="{COLORS[3]}"], [data-b="{COLORS[3]}"]', 1, False),
    (RP, '[data-g="김광일 기자"], [data-b="김광일 기자"]', f'[data-g="{TEAM_SECTION}"], [data-b="{TEAM_SECTION}"]', 1, False),
    # 기기 연동 숨김(GitHub 계정이 없는 기자는 못 쓴다 — 버튼만 숨김)
    (RP, '<button type="button" id="sync" class="sync off"', '<button type="button" id="sync" class="sync off" style="display:none"', 1, False),
    (RP, "<title>뉴스레이다</title>", f"<title>뉴스레이다 · {BEATS_TITLE}</title>", 1, False),
    (RP, '<span class="who">김광일<span class="whob"> (과학·방송·경쟁 담당)</span></span>', WHO, 1, False),
    (RP, "document.title = '뉴스레이다 · ' + r.title;", f"document.title = '{TAB_TITLE} · ' + r.title;", 1, False),
    (RP, "맨 끝 ‘김광일 기자’는", f"맨 끝 ‘{TEAM_SECTION}’은", 1, False),
    (RP, "체크한 기사와 ‘여기까지 확인’은 이 기기에 저장되고, 머리줄 <b>기기 연동</b>을 켜면 다른 기기와 맞춰집니다(내 GitHub 비공개 gist). · <a href=\"../\">최신 다이제스트</a> · <a href=\"../archive/\">지난 다이제스트</a></p>",
         "체크한 기사와 ‘여기까지 확인’은 이 기기(브라우저)에만 저장됩니다 — PC와 폰은 따로 기억합니다.</p>", 1, False),
]

COPY_AS_IS = ["merge_db.py", "retitle.py"]

FORBIDDEN = {
    RP: ["nm-live-", "김광일 기자\"", "기기 연동</b>", "방미통위 → 공정위"],
}
EXPECT = {
    "DUTY_COLLECT": False,
    "DUTY_ONLY_GROUPS": [],
    "LIVE_FOLD_KEEP": LT.fold_keep(GROUPS),   # 11/7 02:18 사용자 "접기 걸자"
    "EXCLUDE_TERMS": [],
    "KEYWORDS": LT.keywords_for(GROUPS),
    "KEYWORD_MAX_PAGES": {"CBS": 1, **{k: 0 for k in LT.NO_SEARCH}},
    "GROUP_ORDER": GROUPS,
    "RETENTION_DAYS": 45,
    "BYLINE_NAME": REPORTER,
    "BYLINE_NAMES": TEAM,
    "BYLINE_SECTION": TEAM_SECTION,
    "BYLINE_TRUST_META": True,
    "LIVE_STORY_MERGE_GROUPS": [g for g in LT.STORY_MERGE if g in GROUPS],
    "ACTOR_ASSIGN": True,
    "LIVE_ACTOR_BONUS": 2.0,
    "ACTOR_PEOPLE_SEED": {p: g for p, g in LT.SEED.items() if g in GROUPS},
    "NOCUT_ENABLED": True,
    "LIVE_REGION_FOLD": True,
}


def md5(b):
    return hashlib.md5(b).hexdigest()


def apply(src_dir):
    out = {}
    for fname in {r[0] for r in REPLACEMENTS}:
        with open(os.path.join(src_dir, fname), encoding="utf-8") as f:
            out[fname] = f.read()
    errors = []
    for fname, old, new, count, is_re in REPLACEMENTS:
        text = out[fname]
        found = len(re.findall(old, text)) if is_re else text.count(old)
        if found != count:
            errors.append(f"{fname}: {old[:60]!r} — {count}번이어야 하는데 {found}번")
            continue
        out[fname] = re.sub(old, lambda m: new, text) if is_re else text.replace(old, new)
    if errors:
        raise SystemExit("원본이 예상과 달라 생성을 멈춥니다(아무 파일도 쓰지 않음):\n  " + "\n  ".join(errors))
    leftovers = []
    for fname, pats in FORBIDDEN.items():
        for i, line in enumerate(out[fname].splitlines(), 1):
            s = line.strip()
            if s.startswith("#") or s.startswith("//"):
                continue
            for p in pats:
                if p in line:
                    leftovers.append(f"{fname}:{i}: {p!r} — {s[:80]}")
    if leftovers:
        raise SystemExit("원본 고유 문자열이 남았습니다:\n  " + "\n  ".join(leftovers))
    return out


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    src = os.path.abspath(sys.argv[1])
    dst = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), ".."))
    out = apply(src)
    import json, subprocess, tempfile
    with tempfile.TemporaryDirectory() as tmp:
        for fname, text in out.items():
            with open(os.path.join(tmp, fname), "w", encoding="utf-8") as f:
                f.write(text)
        probe = ("import json, news_monitor as m; print(json.dumps({k: getattr(m, k) for k in %r}, "
                 "ensure_ascii=False, default=list))" % list(EXPECT))
        env = dict(os.environ, DUTY_MODE="")
        r = subprocess.run([sys.executable, "-c", probe], cwd=tmp, env=env, capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit("생성본 import 실패:\n" + r.stderr[-2000:])
        got = json.loads(r.stdout.strip().splitlines()[-1])
        bad = {k: (got.get(k), v) for k, v in EXPECT.items() if got.get(k) != json.loads(json.dumps(v, ensure_ascii=False, default=list))}
        if bad:
            raise SystemExit(f"생성본 설정값이 예상과 다릅니다: {bad}")
    for fname, text in sorted(out.items()):
        with open(os.path.join(dst, fname), "w", encoding="utf-8") as f:
            f.write(text)
    for fname in COPY_AS_IS:
        shutil.copyfile(os.path.join(src, fname), os.path.join(dst, fname))
    for fname in sorted(list(out) + COPY_AS_IS):
        with open(os.path.join(src, fname), "rb") as a, open(os.path.join(dst, fname), "rb") as b:
            print(f"{fname:18s} 원본 {md5(a.read())} → 생성 {md5(b.read())}")


if __name__ == "__main__":
    main()
