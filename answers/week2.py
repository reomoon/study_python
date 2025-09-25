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
        checks.append('✅ 문제 1-1: num 변수에 42가 할당됨')
    else:
        checks.append('❌ 문제 1-1: num이 42인지 확인해주세요')
    import re
    # <class 'int'> 같은 출력에서 \b가 동작하지 않을 수 있어 단순 포함 검사로 변경
    if 'int' in output:
        checks.append('✅ 문제 1-1 출력: 타입 출력 확인')
    else:
        checks.append('❌ 문제 1-1 출력: 타입 출력이 보이지 않습니다')

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
        checks.append('✅ 문제 2-1: 15와 4 값이 있는 변수 확인')
    elif found_15 or found_4:
        checks.append('⚠️ 문제 2-1: 15 또는 4 값만 있음 (부분 점수)')
    else:
        checks.append('❌ 문제 2-1: 15, 4 값이 있는 변수를 찾을 수 없음')
    # 덧셈 결과 19가 출력에 있으면 인정
    if re.search(r"(?<!\d)19(?!\d)", output):
        checks.append('✅ 문제 2-2 출력: 덧셈 결과 출력 확인')
    else:
        # 혹시 15+4가 아닌 다른 방식으로 19가 출력됐을 수도 있으니, 19가 출력에 있으면 부분 점수
        if '19' in output:
            checks.append('⚠️ 문제 2-2 출력: 19가 출력에 있으나 덧셈 결과인지 불명확 (부분 점수)')
        else:
            checks.append('❌ 문제 2-2 출력: 덧셈 결과가 보이지 않습니다')

    # 3) name 변수와 출력 형식
    if module is not None and hasattr(module, 'name') and isinstance(getattr(module,'name'), str):
        checks.append('✅ 문제 3-1: name 변수 정의 완료')
    else:
        checks.append('❌ 문제 3-1: name 변수가 정의되지 않았습니다')
    
    # name 변수의 실제 값이 출력에 포함되어 있는지 확인
    name_output_found = False
    if module is not None and hasattr(module, 'name'):
        actual_name = getattr(module, 'name')
        if isinstance(actual_name, str) and actual_name in output:
            name_output_found = True
    # 또는 "name" 문자열 자체가 출력에 있는지도 확인 (변수명을 직접 출력한 경우)
    if name_output_found or 'name' in output.lower():
        checks.append('✅ 문제 3-2 출력: 이름 출력 형식 확인')
    else:
        checks.append('❌ 문제 3-2 출력: 이름 출력이 형식에 맞지 않습니다')

    list_defined  = False
    len_sum_used = False
    correct_output_found  = False

    # 4-1 numbers 리스트 정의 검증
    if module is not None and hasattr(module, 'numbers') and isinstance(getattr(module,'numbers'), (list,tuple)):
        list_defined  =True
        checks.append('✅ 문제 4-1: numbers 리스트 정의 완료')

        user_list = getattr(module, 'numbers')
        expected_len = len(user_list)
        expected_sum = sum(user_list)

        if str(expected_len) in output or str(expected_sum) in output:
            correct_output_found = True
    else:
        checks.append('❌ 문제 4-1: numbers 리스트를 정의해주세요')

    # 4-2 len() 또는 sum() 함수가 사용되고 출력되는지 검증
    if module is not None and getattr(module, '__source__', None):
        source_code = getattr(module, '__source__', '')
        if 'len(' in source_code or 'sum(' in source_code:
            len_sum_used = True

    if list_defined and len_sum_used and correct_output_found:
        checks.append('✅ 문제 4-2: 리스트 길이나 합이 출력된 것으로 보입니다')
    elif list_defined and len_sum_used:
        checks.append('⚠️ 문제 4-2: 리스트 길이나 합을 구하는 코드는 있으나 출력이 확인되지 않습니다 (부분 점수)')
    else:
        checks.append('❌ 문제 4-2: len() 또는 sum() 함수를 사용하지 않았습니다.')

    # 5) info dict with age and city
    if module is not None and hasattr(module, 'info') and isinstance(getattr(module,'info'), dict):
        info = getattr(module,'info')
        if 'age' in info:
            checks.append('✅ 문제 5-1: info 딕셔너리에 age 포함')
        else:
            checks.append('❌ 문제 5-1: age 키가 info에 없습니다')
    else:
        checks.append('❌ 문제 5-1: info 딕셔너리를 정의해주세요')
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
        checks.append('✅ 문제 5-2 출력: 나이 또는 도시 출력 확인')
    else:
        checks.append('❌ 문제 5-2 출력: info 관련 출력이 보이지 않습니다')

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
