WEEK = 6

def run(week_module):
    import io, contextlib, importlib.util, re

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
    add_ok = False
    # 1. 'add'라는 이름의 함수가 모듈 내에 존재하는지, 호출 가능한지 확인합니다.
    if hasattr(module, 'add') and callable(module.add):
        try:
            # 2. 함수를 직접 호출하고, 출력(print) 내용을 캡처합니다.
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                module.add(2, 3)
            output_result = f.getvalue().strip()
            
            # 3. 캡처된 출력 결과가 '5'와 정확히 일치하는지 확인합니다.
            if output_result == '5':
                add_ok = True
        except Exception:
            # 만약 함수 실행 중 오류가 발생하면, 통과하지 못합니다.
            pass

    if add_ok:
        checks.append('✅ 문제 1: add(a, b) 함수 작성 및 출력 확인')
    else:
        checks.append('❌ 문제 1: add(a, b) 함수 오류 또는 미정의')



    # 2) reverse 함수 존재 및 동작 확인
    if module is not None and callable(module.__dict__.get('reverse')):
        checks.append('✅ 문제 2: reverse 함수 정의 확인')
    else:
        checks.append('❌ 문제 2: reverse 함수가 정의되지 않았습니다')

    # 3) greet 함수 사용 확인
    default_arg_ok = False
    if module is not None and getattr(module, '__source__', None):
        src = module.__source__
        
        # 3번 문제의 정답 패턴 (def greet(name='학생'): return ...)을 찾습니다.
        # 여러 줄에 걸쳐 있을 수 있는 주석, 공백을 고려하여 정규식을 작성합니다.
        pattern = re.compile(r"def\s+greet\s*\(\s*name\s*=\s*['\"]학생['\"]\s*\)\s*:\s*(?:.|\n)*?\s*return\s+f?['\"]안녕하세요,\s*\{\s*name\s*\}\s*['\"]", re.MULTILINE)
        
        # 소스 코드에서 패턴을 찾습니다.
        if pattern.search(src):
            default_arg_ok = True
        
    if default_arg_ok:
        checks.append('✅ 문제 3: 기본값 인자 사용 확인')
    else:
        checks.append('❌ 문제 3: 기본값 인자 오류')

    # 4) docstring 존재 확인
    docstring_ok = False
    for fn_name in ['add', 'reverse', 'greet', 'find_max', 'is_prime', 'count_value']:
        fn = getattr(module, fn_name, None)
        if fn and callable(fn) and getattr(fn, '__doc__', None):
             docstring_ok = True
             break
    if docstring_ok:
        checks.append('✅ 문제 4: __doc__가 채워진 함수 확인')
    else:
        checks.append('❌ 문제 4: 함수 __doc__가 비어있습니다')
    
    # find_max 함수 채점 로직
    find_max_ok = False
    # 5) 'find_max'라는 이름의 함수가 모듈 내에 존재하는지, 호출 가능한지 확인합니다.
    if hasattr(module, 'find_max') and callable(module.find_max):
        try:
            # 2. 함수를 직접 호출하고 반환값을 확인합니다.
            # 다양한 테스트 케이스를 사용하여 견고하게 만듭니다.
            if (module.find_max([1, 5, 3]) == 5 and
                module.find_max([10, 2, 8, 1]) == 10 and
                module.find_max([-1, -5, -2]) == -1):
                find_max_ok = True
        except Exception:
            # 함수 실행 중 오류가 발생하면 통과하지 못합니다.
            pass
    if find_max_ok:
        checks.append('✅ 문제 5: find_max(lst) 함수 작성 및 반환값 확인')
    else:
        checks.append('❌ 문제 5: find_max(lst) 함수 오류 또는 미정의')

    # 6) is_prime 함수 채점 로직
    is_prime_ok = False
    # 'is_prime' 함수가 모듈 내에 존재하고 호출 가능한지 확인합니다.
    if hasattr(module, 'is_prime') and callable(module.is_prime):
        try:
            # 2. 소수인 경우와 소수가 아닌 경우를 모두 테스트합니다.
            prime_test = module.is_prime(7)
            non_prime_test = module.is_prime(8)
            
            # 3. 반환값이 예상과 정확히 일치하는지 확인합니다.
            if prime_test is True and non_prime_test is False:
                is_prime_ok = True
        except Exception:
            # 함수 실행 중 오류가 발생하면 통과하지 못합니다.
            pass
    if is_prime_ok:
        checks.append('✅ 문제 6: is_prime(n) 함수 작성 및 반환값 확인')
    else:
        checks.append('❌ 문제 6: is_prime(n) 함수 오류 또는 미정의')

    # 7) count_value 함수 채점 로직
    count_value_ok = False
    # 'count_value'라는 이름의 함수가 모듈 내에 존재하고 호출 가능한지 확인합니다.
    if hasattr(module, 'count_value') and callable(module.count_value):
        try:
            # 2. 함수를 직접 호출하고 반환값을 확인합니다.
            if (module.count_value([1, 2, 2, 3], 2) == 2 and
                module.count_value([5, 5, 5, 5], 5) == 4 and
                module.count_value([1, 2, 3], 4) == 0):
                count_value_ok = True
        except Exception:
            # 함수 실행 중 오류가 발생하면 통과하지 못합니다.
            pass
    if count_value_ok:
        checks.append('✅ 문제 7: count_value(lst, value) 함수 작성 및 반환값 확인')
    else:
        checks.append('❌ 문제 7: count_value(lst, value) 함수 오류 또는 미정의')

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
