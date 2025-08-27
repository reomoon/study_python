WEEK = 1

def _compute_comment_score_from_source(src_lines):
    total_lines = len(src_lines)
    comment_lines = 0
    code_lines = 0
    meaningful_comments = 0
    for line in src_lines:
        stripped = line.strip()
        if stripped.startswith('#'):
            comment_lines += 1
            if (stripped != '#' and '답을 아래에 작성하세요' not in stripped and '문제' not in stripped and len(stripped) > 10):
                meaningful_comments += 1
        elif stripped and not stripped.startswith('#'):
            code_lines += 1

    comment_ratio = (comment_lines * 100 // code_lines) if code_lines > 0 else 0
    score = 0
    if comment_ratio >= 15:
        score += 2
    elif comment_ratio >= 8:
        score += 1
    if meaningful_comments >= 1:
        score += 1
    return score

def run(week_module):
    """Run week1 checks. week_module may be an in-memory module injected by app.py."""
    import importlib.util, sys, io, contextlib, os

    # Load week module (memory preferred)
    output = ''
    week1 = None
    if week_module is not None:
        week1 = week_module
        src = getattr(week1, '__source__', None)
        if src is not None:
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                try:
                    exec(src, week1.__dict__)
                except Exception as e:
                    print(f"❌ 코드 실행 중 오류: {e}")
            output = f.getvalue()
    if week1 is None:
        # try file fallback (root) then examples/
        tried = False
        try:
            spec = importlib.util.spec_from_file_location("week1", "week1_variable.py")
            week1 = importlib.util.module_from_spec(spec)
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                spec.loader.exec_module(week1)
            output = f.getvalue()
            tried = True
        except Exception:
            week1 = None
        if week1 is None:
            try:
                spec = importlib.util.spec_from_file_location("week1", "examples/week1_example.py")
                week1 = importlib.util.module_from_spec(spec)
                f = io.StringIO()
                with contextlib.redirect_stdout(f):
                    spec.loader.exec_module(week1)
                output = f.getvalue()
                tried = True
            except Exception:
                week1 = None

    checks = []
    import re
    # 문제 1: x=7
    found_7 = False
    if week1 is not None:
        for var in dir(week1):
            if not var.startswith('__'):
                val = getattr(week1, var)
                if isinstance(val, (int, float)) and val == 7:
                    found_7 = True
    if found_7:
        checks.append("✅ 문제 1: 7 값이 있는 변수 확인")
    else:
        checks.append("❌ 문제 1: 7 값이 있는 변수를 찾을 수 없음")
    if re.search(r"(?<!\d)7(?!\d)", output):
        checks.append("✅ 문제 1 출력: 7 출력 확인")
    elif '7' in output:
        checks.append("⚠️ 문제 1 출력: 7이 출력에 있으나 형식 불명확 (부분 점수)")
    else:
        checks.append("❌ 문제 1 출력: 7 출력이 없음")

    # 문제 2: a=3, b=8, 곱=24
    found_3 = False
    found_8 = False
    found_24 = False
    if week1 is not None:
        for var in dir(week1):
            if not var.startswith('__'):
                val = getattr(week1, var)
                if isinstance(val, (int, float)):
                    if val == 3:
                        found_3 = True
                    if val == 8:
                        found_8 = True
                    if val == 24:
                        found_24 = True
    if found_3 and found_8:
        checks.append("✅ 문제 2: 3과 8 값이 있는 변수 확인")
    elif found_3 or found_8:
        checks.append("⚠️ 문제 2: 3 또는 8 값만 있음 (부분 점수)")
    else:
        checks.append("❌ 문제 2: 3, 8 값이 있는 변수를 찾을 수 없음")
    if re.search(r"(?<!\d)24(?!\d)", output):
        checks.append("✅ 문제 2 출력: 곱 24 출력 확인")
    elif '24' in output:
        checks.append("⚠️ 문제 2 출력: 24가 출력에 있으나 형식 불명확 (부분 점수)")
    else:
        checks.append("❌ 문제 2 출력: 곱 결과가 출력되지 않음")

    # 문제 3: name='홍길동', "내 이름은"
    found_name = False
    if week1 is not None:
        for var in dir(week1):
            if not var.startswith('__'):
                val = getattr(week1, var)
                if isinstance(val, str) and ('홍길동' in val or '길동' in val):
                    found_name = True
    if found_name:
        checks.append("✅ 문제 3: 이름 변수에 홍길동 포함 확인")
    else:
        checks.append("❌ 문제 3: 이름 변수에 홍길동이 없음")
    if "내 이름은" in output:
        checks.append("✅ 문제 3 출력: 이름 출력 형식 확인")
    elif "이름" in output:
        checks.append("⚠️ 문제 3 출력: 이름 관련 출력 있으나 형식 불명확 (부분 점수)")
    else:
        checks.append("❌ 문제 3 출력: 이름 출력 없음")

    # 문제 4: width=5, height=10, 넓이=50
    found_5 = False
    found_10 = False
    found_50 = False
    if week1 is not None:
        for var in dir(week1):
            if not var.startswith('__'):
                val = getattr(week1, var)
                if isinstance(val, (int, float)):
                    if val == 5:
                        found_5 = True
                    if val == 10:
                        found_10 = True
                    if val == 50:
                        found_50 = True
    if found_5 and found_10:
        checks.append("✅ 문제 4: 5와 10 값이 있는 변수 확인")
    elif found_5 or found_10:
        checks.append("⚠️ 문제 4: 5 또는 10 값만 있음 (부분 점수)")
    else:
        checks.append("❌ 문제 4: 5, 10 값이 있는 변수를 찾을 수 없음")
    if re.search(r"(?<!\d)50(?!\d)", output):
        checks.append("✅ 문제 4 출력: 넓이 50 출력 확인")
    elif '50' in output:
        checks.append("⚠️ 문제 4 출력: 50이 출력에 있으나 형식 불명확 (부분 점수)")
    else:
        checks.append("❌ 문제 4 출력: 넓이 결과가 출력되지 않음")

    # 문제 5: temp=36.5, "체온"
    found_temp = False
    if week1 is not None:
        for var in dir(week1):
            if not var.startswith('__'):
                val = getattr(week1, var)
                if isinstance(val, (int, float)) and abs(val - 36.5) < 0.01:
                    found_temp = True
    if found_temp:
        checks.append("✅ 문제 5: 36.5 값이 있는 변수 확인")
    else:
        checks.append("❌ 문제 5: 36.5 값이 있는 변수를 찾을 수 없음")
    if "체온" in output and re.search(r"36\.5", output):
        checks.append("✅ 문제 5 출력: 체온 출력 형식 확인")
    elif "체온" in output or "36.5" in output:
        checks.append("⚠️ 문제 5 출력: 체온 관련 출력 있으나 형식 불명확 (부분 점수)")
    else:
        checks.append("❌ 문제 5 출력: 체온 출력 없음")

    for c in checks:
        print(c)

    # comment score
    comment_score = 0
    src_lines = None
    if week1 is not None and getattr(week1, '__source__', None):
        src_lines = week1.__source__.splitlines()
    else:
        try:
            with open('week1_variable.py', 'r', encoding='utf-8') as f:
                src_lines = f.read().splitlines()
        except Exception:
            src_lines = []
    comment_score = _compute_comment_score_from_source(src_lines)
    print("\n💬 주석 품질 검사:")
    print(f"   - 주석 점수: {comment_score}")

    total_score = len([c for c in checks if c.startswith("✅")]) + comment_score
    return total_score
