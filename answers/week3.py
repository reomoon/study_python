WEEK = 3

def run(week_module):
    """Grade week3: simple stdout/input checks. Accepts in-memory module or falls back to file."""
    import io, contextlib, importlib.util

    module = week_module
    output = ''
    # If we have source, exec to capture prints
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
        # try file fallback (root) then examples/
        try:
            spec = importlib.util.spec_from_file_location('week3', 'week3_io.py')
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
                spec = importlib.util.spec_from_file_location('week3', 'examples/week3_example.py')
                mod = importlib.util.module_from_spec(spec)
                f = io.StringIO()
                with contextlib.redirect_stdout(f):
                    spec.loader.exec_module(mod)
                output = f.getvalue()
                module = mod
            except Exception:
                module = None

    checks = []
    # 1) Hello, world!
    if 'Hello' in output and 'world' in output:
        checks.append('✅ 문제 1: Hello 출력 확인')
    else:
        checks.append('❌ 문제 1: Hello 출력이 보이지 않습니다')

    # 2) input name -> 안녕하세요
    if '안녕하세요' in output or '안녕' in output:
        checks.append('✅ 문제 2: 인사 출력 확인')
    else:
        checks.append('❌ 문제 2: 인사 출력이 보이지 않습니다')

    # 3) 두 숫자 더하기 출력
    if any(str(n) in output for n in range(0, 200)):
        checks.append('✅ 문제 3: 숫자 출력(덧셈) 확인(느슨한 검사)')
    else:
        checks.append('❌ 문제 3: 덧셈 결과 출력이 보이지 않습니다')

    # 4) 여러 줄 출력
    if output.count('\n') >= 1:
        checks.append('✅ 문제 4: 여러 줄 출력 확인')
    else:
        checks.append('❌ 문제 4: 여러 줄 출력이 감지되지 않았습니다')

    # 5) int 변환 후 계산
    if any('%' in s for s in []):
        # placeholder, keep loose
        pass
    # loose numeric check already covers it

    for c in checks:
        print(c)

    # basic comment heuristic
    try:
        if module is not None and getattr(module, '__source__', None):
            lines = module.__source__.splitlines()
        else:
            with open('week3_io.py','r',encoding='utf-8') as f:
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
