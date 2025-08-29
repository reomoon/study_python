# --- 재점기: problem_week5.html 기준 ---
import io, contextlib, importlib.util, re
def grade_week5_v2(module_path):
    spec = importlib.util.spec_from_file_location('week5', module_path)
    mod = importlib.util.module_from_spec(spec)
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        spec.loader.exec_module(mod)
    output = f.getvalue()
    checks = []
    # 1. 1~5까지 출력
    if re.search(r"\b1\b.*\b2\b.*\b3\b.*\b4\b.*\b5\b", output, flags=re.DOTALL):
        checks.append('✅ 문제 1: 1~5까지 출력 확인')
    else:
        checks.append('❌ 문제 1: 1~5까지 출력 없음')
    # 2. 리스트 합
    if re.search(r"\b15\b", output) or re.search(r"sum", output) or re.search(r"합", output):
        checks.append('✅ 문제 2: 리스트 합 출력 확인')
    else:
        checks.append('❌ 문제 2: 리스트 합 출력 없음')
    # 3. while 카운트다운
    if re.search(r"3\s*2\s*1\s*0", output):
        checks.append('✅ 문제 3: while 카운트다운 출력 확인')
    else:
        checks.append('❌ 문제 3: 카운트다운 출력 없음')
    # 4. 리스트 컴프리헨션 제곱 리스트
    if re.search(r"\[1, 4, 9, 16, 25\]", output):
        checks.append('✅ 문제 4: 제곱 리스트 출력 확인')
    else:
        checks.append('❌ 문제 4: 제곱 리스트 출력 없음')
    # 5. 구구단 2~9단, 1~9 곱셈
    gugudan_ok = True
    for i in range(2, 10):
        for j in range(1, 10):
            pattern = fr"{i} x {j} = {i*j}"
            if not re.search(pattern, output):
                gugudan_ok = False
                break
        if not gugudan_ok:
            break
    if gugudan_ok:
        checks.append('✅ 문제 5: 구구단 전체 출력 확인')
    else:
        checks.append('❌ 문제 5: 구구단 출력 일부 누락')
    # 6. break/continue 사용
    code = open(module_path, encoding='utf-8').read()
    if 'break' in code and 'continue' in code:
        checks.append('✅ 문제 6: break/continue 모두 사용')
    elif 'break' in code or 'continue' in code:
        checks.append('✅ 문제 6: break 또는 continue 사용')
    else:
        checks.append('❌ 문제 6: break/continue 사용 없음')
    for c in checks:
        print(c)
    return sum(c.startswith('✅') for c in checks)
WEEK = 5

def run(week_module):
    import io, contextlib, importlib.util

    module = week_module
    output = ''
    if module is not None and getattr(module, '__source__', None):
        src = module.__source__
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            try:
                exec(src, module.__dict__)
            except Exception as e:
                print(f"❌ 코드 실행 오류: {e}")
        output = f.getvalue()
    else:
        try:
            spec = importlib.util.spec_from_file_location('week5', 'week5_loop.py')
            mod = importlib.util.module_from_spec(spec)
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                spec.loader.exec_module(mod)
            output = f.getvalue()
            module = mod
        except Exception:
            module = None
        if module is None:
            try:
                spec = importlib.util.spec_from_file_location('week5', 'examples/week5_example.py')
                mod = importlib.util.module_from_spec(spec)
                f = io.StringIO()
                with contextlib.redirect_stdout(f):
                    spec.loader.exec_module(mod)
                output = f.getvalue()
                module = mod
            except Exception:
                module = None

    import re
    checks = []
    # 1. 1~5까지 출력
    if re.search(r"\b1\b.*\b2\b.*\b3\b.*\b4\b.*\b5\b", output, flags=re.DOTALL):
        checks.append('✅ 문제 1: 1~5까지 출력 확인')
    else:
        checks.append('❌ 문제 1: 1~5까지 출력 없음')
    # 2. 리스트 합
    if re.search(r"\b15\b", output) or re.search(r"sum", output) or re.search(r"합", output):
        checks.append('✅ 문제 2: 리스트 합 출력 확인')
    else:
        checks.append('❌ 문제 2: 리스트 합 출력 없음')
    # 3. while 카운트다운
    if re.search(r"3\s*2\s*1\s*0", output):
        checks.append('✅ 문제 3: while 카운트다운 출력 확인')
    else:
        checks.append('❌ 문제 3: 카운트다운 출력 없음')
    # 4. 리스트 컴프리헨션 제곱 리스트
    if re.search(r"\[1, 4, 9, 16, 25\]", output):
        checks.append('✅ 문제 4: 제곱 리스트 출력 확인')
    else:
        checks.append('❌ 문제 4: 제곱 리스트 출력 없음')
    # 5. 구구단 2~9단, 1~9 곱셈
    gugudan_ok = True
    for i in range(2, 10):
        for j in range(1, 10):
            pattern = fr"{i} x {j} = {i*j}"
            if not re.search(pattern, output):
                gugudan_ok = False
                break
        if not gugudan_ok:
            break
    if gugudan_ok:
        checks.append('✅ 문제 5: 구구단 전체 출력 확인')
    else:
        checks.append('❌ 문제 5: 구구단 출력 일부 누락')
    # 6. break/continue 사용
    code = module.__source__ if module and getattr(module,'__source__',None) else ''
    if 'break' in code and 'continue' in code:
        checks.append('✅ 문제 6: break/continue 모두 사용')
    elif 'break' in code or 'continue' in code:
        checks.append('✅ 문제 6: break 또는 continue 사용')
    else:
        checks.append('❌ 문제 6: break/continue 사용 없음')
    for c in checks:
        print(c)
    return sum(c.startswith('✅') for c in checks)
