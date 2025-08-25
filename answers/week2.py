WEEK = 2

def run(week_module):
    """Grade week2. Accepts an in-memory module (from app) or falls back to file."""
    import importlib.util, io, contextlib, os

    # try memory module first
    output = ''
    module = None
    if week_module is not None:
        module = week_module
        src = getattr(module, '__source__', None)
        if src is not None:
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                try:
                    exec(src, module.__dict__)
                except Exception as e:
                    print(f"❌ 코드 실행 오류: {e}")
            output = f.getvalue()

    if module is None:
        # try root file then examples/
        try:
            spec = importlib.util.spec_from_file_location('week2', 'week2_datatype.py')
            module = importlib.util.module_from_spec(spec)
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                spec.loader.exec_module(module)
            output = f.getvalue()
        except Exception:
            module = None
        if module is None:
            try:
                spec = importlib.util.spec_from_file_location('week2', 'examples/week2_example.py')
                module = importlib.util.module_from_spec(spec)
                f = io.StringIO()
                with contextlib.redirect_stdout(f):
                    spec.loader.exec_module(module)
                output = f.getvalue()
            except Exception:
                module = None

    checks = []

    # 1) num = 42 and type printed
    if module is not None and hasattr(module, 'num') and getattr(module, 'num') == 42:
        checks.append('✅ 문제 1: num 변수에 42가 할당됨')
    else:
        checks.append('❌ 문제 1: num이 42인지 확인해주세요')
    if 'int' in output:
        checks.append('✅ 문제 1 출력: 타입 출력 확인')
    else:
        checks.append('❌ 문제 1 출력: 타입 출력이 보이지 않습니다')

    # 2) a=15,b=4 and sum printed
    if module is not None and hasattr(module, 'a') and hasattr(module, 'b') and (getattr(module,'a')==15 and getattr(module,'b')==4):
        checks.append('✅ 문제 2: a,b 변수 설정 완료')
    else:
        checks.append('❌ 문제 2: a,b 변수 설정을 확인해주세요')
    if '19' in output:
        checks.append('✅ 문제 2 출력: 덧셈 결과 출력 확인')
    else:
        checks.append('❌ 문제 2 출력: 덧셈 결과가 보이지 않습니다')

    # 3) name 변수와 출력 형식
    if module is not None and hasattr(module, 'name') and isinstance(getattr(module,'name'), str):
        checks.append('✅ 문제 3: name 변수 정의 완료')
    else:
        checks.append('❌ 문제 3: name 변수가 정의되지 않았습니다')
    if '내 이름은' in output:
        checks.append('✅ 문제 3 출력: 이름 출력 형식 확인')
    else:
        checks.append('❌ 문제 3 출력: 이름 출력이 형식에 맞지 않습니다')

    # 4) numbers list and length/sum printed
    if module is not None and hasattr(module, 'numbers') and isinstance(getattr(module,'numbers'), (list,tuple)):
        checks.append('✅ 문제 4: numbers 리스트 정의 완료')
    else:
        checks.append('❌ 문제 4: numbers 리스트를 정의해주세요')
    if 'len' in output or 'sum' in output or any(str(x) in output for x in [0,1,2,3,4,5,6,7,8,9]):
        # loose check: any numeric output appears
        checks.append('✅ 문제 4 출력: 리스트 길이나 합이 출력된 것으로 보입니다')
    else:
        checks.append('❌ 문제 4 출력: 리스트 관련 출력이 보이지 않습니다')

    # 5) info dict with age and city
    if module is not None and hasattr(module, 'info') and isinstance(getattr(module,'info'), dict):
        info = getattr(module,'info')
        if 'age' in info:
            checks.append('✅ 문제 5: info 딕셔너리에 age 포함')
        else:
            checks.append('❌ 문제 5: age 키가 info에 없습니다')
    else:
        checks.append('❌ 문제 5: info 딕셔너리를 정의해주세요')
    if 'age' in output or 'city' in output:
        checks.append('✅ 문제 5 출력: 나이 또는 도시 출력 확인')
    else:
        checks.append('❌ 문제 5 출력: info 관련 출력이 보이지 않습니다')

    for c in checks:
        print(c)

    # simple comment scoring reuse
    comment_score = 0
    try:
        if module is not None and getattr(module, '__source__', None):
            lines = module.__source__.splitlines()
        else:
            with open('week2_datatype.py','r',encoding='utf-8') as f:
                lines = f.read().splitlines()
    except Exception:
        lines = []

    # small heuristic
    comment_lines = sum(1 for l in lines if l.strip().startswith('#'))
    code_lines = sum(1 for l in lines if l.strip() and not l.strip().startswith('#'))
    if code_lines > 0:
        ratio = comment_lines * 100 // code_lines
        if ratio >= 15:
            comment_score = 2
        elif ratio >= 8:
            comment_score = 1

    total = len([c for c in checks if c.startswith('✅')]) + comment_score
    return total
