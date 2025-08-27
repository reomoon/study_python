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
    import re
    # <class 'int'> 같은 출력에서 \b가 동작하지 않을 수 있어 단순 포함 검사로 변경
    if 'int' in output:
        checks.append('✅ 문제 1 출력: 타입 출력 확인')
    else:
        checks.append('❌ 문제 1 출력: 타입 출력이 보이지 않습니다')

    # 2) a=15, b=4, 덧셈 결과 19 출력 (유연하게 평가)
    found_15 = False
    found_4 = False
    # 변수명에 관계없이 값이 15, 4인 int형 변수가 있으면 인정
    if module is not None:
        for var in dir(module):
            if not var.startswith('__'):
                val = getattr(module, var)
                if isinstance(val, int):
                    if val == 15:
                        found_15 = True
                    if val == 4:
                        found_4 = True
    if found_15 and found_4:
        checks.append('✅ 문제 2: 15와 4 값이 있는 변수 확인')
    elif found_15 or found_4:
        checks.append('⚠️ 문제 2: 15 또는 4 값만 있음 (부분 점수)')
    else:
        checks.append('❌ 문제 2: 15, 4 값이 있는 변수를 찾을 수 없음')
    # 덧셈 결과 19가 출력에 있으면 인정
    if re.search(r"(?<!\d)19(?!\d)", output):
        checks.append('✅ 문제 2 출력: 덧셈 결과 출력 확인')
    else:
        # 혹시 15+4가 아닌 다른 방식으로 19가 출력됐을 수도 있으니, 19가 출력에 있으면 부분 점수
        if '19' in output:
            checks.append('⚠️ 문제 2 출력: 19가 출력에 있으나 덧셈 결과인지 불명확 (부분 점수)')
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
    if re.search(r"len\s*\(|sum\s*\(|\d+", output):
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
    # 출력 검사: 'age' 또는 'city' 단어 또는 info에 담긴 값(예: 25)이 출력에 보이면 통과
    printed_ok = False
    try:
        if 'age' in output or 'city' in output:
            printed_ok = True
        elif module is not None and getattr(module, 'info', None):
            info = getattr(module, 'info')
            if isinstance(info, dict):
                if 'age' in info and str(info.get('age')) in output:
                    printed_ok = True
                if 'city' in info and str(info.get('city')) in output:
                    printed_ok = True
    except Exception:
        printed_ok = False
    if printed_ok:
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
