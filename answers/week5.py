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
    # 1) 1~5 출력: 정확한 숫자 시퀀스가 있는지 확인(간단히 첫 줄에서)
    if re.search(r"\b1\b.*\b2\b.*\b3\b", output, flags=re.DOTALL):
        checks.append('✅ 문제 1: 1~5 출력 감지')
    else:
        checks.append('❌ 문제 1: 1~5 출력이 보이지 않습니다')

    # 2) 리스트 합: 정확한 합 숫자(예: 15) 또는 'sum' 키워드
    if re.search(r"\b15\b", output) or re.search(r"\bsum\b", output) or re.search(r"합", output):
        checks.append('✅ 문제 2: 리스트 합 출력 확인')
    else:
        checks.append('❌ 문제 2: 리스트 합 출력이 보이지 않습니다')

    if 'while' in (module.__dict__ if module else {}):
        checks.append('✅ 문제 3: while 사용 여부(코드 기반)')
    else:
        # check for countdown pattern
        if any('0' in s for s in output.split()):
            checks.append('✅ 문제 3: while/카운트다운 출력 감지')
        else:
            checks.append('❌ 문제 3: 카운트다운 출력이 보이지 않습니다')

    if re.search(r"\[.*\]", output) and (re.search(r"\*\*", output) or re.search(r"square", output, flags=re.IGNORECASE)):
        checks.append('✅ 문제 4: 제곱 리스트 출력 감지')
    else:
        checks.append('❌ 문제 4: 제곱 리스트 출력이 보이지 않습니다')

    if 'break' in (module.__source__ if module and getattr(module,'__source__',None) else '') or 'continue' in (module.__source__ if module and getattr(module,'__source__',None) else ''):
        checks.append('✅ 문제 5: break/continue 사용 확인')
    else:
        checks.append('❌ 문제 5: break/continue 사용 예가 보이지 않습니다')

    for c in checks:
        print(c)

    # comment heuristic
    try:
        if module is not None and getattr(module,'__source__',None):
            lines = module.__source__.splitlines()
        else:
            with open('week5_loop.py','r',encoding='utf-8') as f:
                lines = f.read().splitlines()
    except Exception:
        lines = []
    comment_lines = sum(1 for l in lines if l.strip().startswith('#'))
    code_lines = sum(1 for l in lines if l.strip() and not l.strip().startswith('#'))
    comment_score = 0
    if code_lines > 0:
        ratio = comment_lines * 100 // code_lines
        if ratio >= 15:
            comment_score = 2
        elif ratio >= 8:
            comment_score = 1

    total = len([c for c in checks if c.startswith('✅')]) + comment_score
    return total
