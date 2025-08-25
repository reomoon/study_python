WEEK = 9

def run(week_module):
    import io, contextlib, importlib.util, os

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
            spec = importlib.util.spec_from_file_location('week9', 'week9_fileio.py')
            mod = importlib.util.module_from_spec(spec)
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                spec.loader.exec_module(mod)
            output = f.getvalue()
            module = mod
        except Exception:
            module = None

    checks = []
    if 'open' in (module.__source__ if module and getattr(module,'__source__',None) else ''):
        checks.append('✅ 문제 1/2: 파일 열기/쓰기/읽기 사용 감지')
    else:
        checks.append('❌ 문제 1/2: 파일 입출력 코드가 보이지 않습니다')

    if 'except' in (module.__source__ if module and getattr(module,'__source__',None) else ''):
        checks.append('✅ 문제 3: 예외 처리 코드 감지')
    else:
        checks.append('❌ 문제 3: 파일 예외 처리 코드가 보이지 않습니다')

    if 'append' in (module.__source__ if module and getattr(module,'__source__',None) else '') or 'a+' in (module.__source__ if module and getattr(module,'__source__',None) else ''):
        checks.append('✅ 문제 5: append 모드 사용 감지')
    else:
        checks.append('❌ 문제 5: append 사용 예가 보이지 않습니다')

    if 'read' in output or 'lines' in output or 'len' in output:
        checks.append('✅ 문제 4: 파일 내용 읽기 및 길이 출력 감지')
    else:
        checks.append('❌ 문제 4: 파일 읽기 출력이 보이지 않습니다')

    for c in checks:
        print(c)

    # comment heuristic
    try:
        if module is not None and getattr(module, '__source__', None):
            lines = module.__source__.splitlines()
        else:
            with open('week9_fileio.py','r',encoding='utf-8') as f:
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
