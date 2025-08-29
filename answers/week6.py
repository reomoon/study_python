WEEK = 6

def run(week_module):
    import io, contextlib, importlib.util

    checks = []
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
            spec = importlib.util.spec_from_file_location('week6', 'week6_funcs.py')
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
                spec = importlib.util.spec_from_file_location('week6', 'examples/week6_example.py')
                mod = importlib.util.module_from_spec(spec)
                f = io.StringIO()
                with contextlib.redirect_stdout(f):
                    spec.loader.exec_module(mod)
                output = f.getvalue()
                module = mod
            except Exception:
                module = None
    # ...existing code...
    # 1) add 함수가 실제로 callable인지 확인
    if module is not None and callable(module.__dict__.get('add')):
        checks.append('✅ 문제 1: add 함수 정의 확인')
    else:
        checks.append('❌ 문제 1: add 함수가 정의되지 않았습니다')

    if module is not None and callable(module.__dict__.get('reverse')):
        checks.append('✅ 문제 2: reverse 함수 정의 확인')
    else:
        checks.append('❌ 문제 2: reverse 함수가 정의되지 않았습니다')

    # 4) default arg — 좀 더 구체적으로 'def name(arg=...' 형태 검사
    import re
    if re.search(r"def\s+\w+\s*\([^)]*=", src, re.IGNORECASE):
        checks.append('✅ 문제 4: 기본값 인자 사용 감지')
    else:
        checks.append('❌ 문제 4: 기본값 인자 사용 예가 보이지 않습니다')

    # 5) docstring 존재 확인
    docs_ok = False
    for n in ['add','reverse']:
        fn = module.__dict__.get(n)
        if fn and getattr(fn,'__doc__',None):
            docs_ok = True
            break
    if docs_ok:
        checks.append('✅ 문제 5: __doc__가 채워진 함수 확인')
    else:
        checks.append('❌ 문제 5: 함수 __doc__가 비어있습니다')

    for c in checks:
        print(c)

    # comment heuristic
    try:
        if module is not None and getattr(module, '__source__', None):
            lines = module.__source__.splitlines()
        else:
            with open('week6_funcs.py','r',encoding='utf-8') as f:
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
