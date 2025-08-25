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

    checks = []
    if any('1' in line for line in output.splitlines()):
        checks.append('✅ 문제 1: 1~5 출력 감지(느슨한 검사)')
    else:
        checks.append('❌ 문제 1: 1~5 출력이 보이지 않습니다')

    if any('sum' in line or '합' in line or any(d in output for d in ['15','10']) for line in output.splitlines()):
        checks.append('✅ 문제 2: 리스트 합 출력(느슨한 검사)')
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

    if '[' in output and any('**' in l or 'square' in l.lower() for l in output.splitlines()):
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
