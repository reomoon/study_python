WEEK = 4

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
            spec = importlib.util.spec_from_file_location('week4', 'week4_condition.py')
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
                spec = importlib.util.spec_from_file_location('week4', 'examples/week4_example.py')
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

    # 1) 짝수/홀수 관련 출력: 부분 문자열, 대소문자 무시
    if re.search(r"짝|홀", output, re.IGNORECASE):
        checks.append('✅ 문제 1: 짝수/홀수 판별 출력 확인')
    else:
        checks.append('❌ 문제 1: 짝수/홀수 출력이 보이지 않습니다')

    # 2) 영/음수/양수: 부분 문자열, 대소문자 무시
    if re.search(r"영|음수|양수", output, re.IGNORECASE):
        checks.append('✅ 문제 2: 영/음수/양수 판별 출력 확인')
    else:
        checks.append('❌ 문제 2: 영/음수/양수 출력이 보이지 않습니다')

    # 3) 예외 처리: 다양한 표현 허용
    if re.search(r"입력 오류|ValueError|예외|오류|에러", output, re.IGNORECASE):
        checks.append('✅ 문제 3: 예외 처리 출력 확인')
    else:
        checks.append('❌ 문제 3: 예외 처리 코드 또는 출력이 보이지 않습니다')

    # 4) 10 포함 여부: 부분 문자열
    if re.search(r"10", output):
        checks.append('✅ 문제 4: 10 비교 관련 출력 감지')
    else:
        checks.append('❌ 문제 4: 10 비교 출력이 보이지 않습니다')

    # 5) 에러/Exception/오류/예외 등 다양한 단어 허용
    if re.search(r"에러|Exception|오류|예외", output, re.IGNORECASE):
        checks.append('✅ 문제 5: 에러 발생/처리 출력 확인')
    else:
        checks.append('❌ 문제 5: 에러 처리 출력이 보이지 않습니다')

    for c in checks:
        print(c)

    # comment heuristic
    try:
        if module is not None and getattr(module, '__source__', None):
            lines = module.__source__.splitlines()
        else:
            with open('week4_condition.py','r',encoding='utf-8') as f:
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
