WEEK = 6

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
            spec = importlib.util.spec_from_file_location('week6', 'week6_funcs.py')
            mod = importlib.util.module_from_spec(spec)
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                spec.loader.exec_module(mod)
            output = f.getvalue()
            module = mod
        except Exception:
            module = None

    checks = []
    # add
    if module is not None and 'add' in module.__dict__:
        checks.append('✅ 문제 1: add 함수 정의 확인')
    else:
        checks.append('❌ 문제 1: add 함수가 정의되지 않았습니다')

    if 'reverse' in (module.__dict__ if module else {}):
        checks.append('✅ 문제 2: reverse 함수 정의 확인')
    else:
        checks.append('❌ 문제 2: reverse 함수가 정의되지 않았습니다')

    if 'import' in (module.__source__ if module and getattr(module,'__source__',None) else ''):
        checks.append('✅ 문제 3: import 사용 예 감지')
    else:
        checks.append('❌ 문제 3: import 사용 예가 보이지 않습니다')

    # 4) default arg
    if 'def ' in (module.__source__ if module and getattr(module,'__source__',None) else '') and '=' in (module.__source__ if module and getattr(module,'__source__',None) else ''):
        checks.append('✅ 문제 4: 기본값 인자 사용 감지(느슨한 검사)')
    else:
        checks.append('❌ 문제 4: 기본값 인자 사용 예가 보이지 않습니다')

    # 5) docstring
    if module is not None and any(getattr(module.__dict__.get(n),'__doc__',None) for n in ['add','reverse']):
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
