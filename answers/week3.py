WEEK = 3

import io, contextlib, builtins, types, importlib.util, re

def run(week_module, student_outputs, stdin_lines):
    """Grade week3: simple stdout/input checks. Accepts in-memory module or falls back to file."""
    input_iter = iter(stdin_lines)
    output_iter = iter(student_outputs)

    module = week_module
    output = output_iter
    # If we have source, exec to capture prints
    if module is not None and getattr(module, '__source__', None):
        src = module.__source__
        
        def _input(prompt=''):
            try:
                value = next(input_iter)
                print(f"[LOG] input 호출, 반환값: {value}")
                return value
            except StopIteration:
                print("[LOG] 입력값이 2개 미만")
                return ''
            
        # input()이 호출되면 '테스트값' 반환
        original_input = module.__dict__.get('input', builtins.input)
        module.__dict__['input'] = _input
        
        # 모든 출력을 StringIO에 담기 위한 버퍼
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            try:
                # 학생 코드 한번만 실행
                exec(src, module.__dict__)
            except ValueError as e:
                print(f"❌ 실행 중 ValueError 발생: {e}")   
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
    
    # 채점 시작
    checks = []
    # 1) Hello, world! (phrase match)
    if re.search(r"Hello\s*,?\s*world", output, flags=re.IGNORECASE):
        checks.append('✅ 문제 1: Hello 출력 확인')
    else:
        checks.append('❌ 문제 1: Hello 출력이 보이지 않습니다')

    # 2) input name -> 인사 출력 (한글/영어 인사 모두 허용)
    if "input(" in src and re.search(r"안녕하세요", src):
        if re.search(r"안녕[하세요]*", output) or re.search(r"\bhi\b|\bhello\b|안녕하세요", output, flags=re.IGNORECASE):
            checks.append('✅ 문제 2: 인사 출력 확인')
        else:
            checks.append('❌ 문제 2: 인사 출력이 보이지 않습니다')
    else:
        checks.append('❌ 문제 2: 이름 입력(input) 기능이 없습니다')

    # 3) 두 숫자 더하기 출력
    # 덧셈 문제 코드가 있는지 먼저 감지합니다.
    if re.search(r"int\(input", src) and re.search(r"\+", src):
        try:
            # 입력값에서 숫자만 추출하여 순서에 구애받지 않습니다.
            numeric_inputs = [int(line.strip()) for line in stdin_lines if line.strip().isdigit()]
            
            if len(numeric_inputs) >= 2:
                # 숫자 입력값이 2개 이상이면 첫 두 값을 덧셈에 사용
                a = numeric_inputs[0]
                b = numeric_inputs[1]
                expected_sum = a + b
                
                if re.search(r'\b' + str(expected_sum) + r'\b', output):
                    checks.append('✅ 문제 3: 숫자 출력(덧셈) 확인')
                else:
                    checks.append('❌ 문제 3: 덧셈 결과가 올바르지 않거나 출력되지 않았습니다.')
            else:
                checks.append('❌ 문제 3: 덧셈에 필요한 두 개의 숫자 입력이 부족합니다.')
        except (ValueError, IndexError):
            checks.append('❌ 문제 3: 입력값 처리 또는 변환 오류')
    else:
        checks.append('❌ 문제 3: 덧셈 코드가 보이지 않습니다.')

    # 4) 여러 줄 출력
    # 문제의 정답 키워드를 정의합니다.
    keyword = "FASHIONGO"

    # 소스 코드에서 파일 입출력 키워드('open', 'read')가 사용되지 않았는지 확인합니다.
    has_file_io = re.search(r"open\s*\(|read\s*\(", src)

    # 학생의 전체 출력에서 키워드의 등장 횟수를 셉니다.
    keyword_count = output.count(keyword)

    # 조건 검사:
    # 1. 파일 입출력이 사용되지 않았는가?
    # 2. 'FASHIONGO' 키워드가 2번 이상 출력되었는가?
    if not has_file_io and keyword_count >= 2:
        checks.append('✅ 문제 4: 키워드를 여러 줄로 출력했습니다.')
    elif not has_file_io and keyword_count > 0:
        checks.append('❌ 문제 4: 키워드가 한 번만 출력되었습니다.')
    else:
        checks.append('❌ 문제 4: 키워드가 출력되지 않았거나 조건을 만족하지 않습니다.')

    # 5) int 변환 후 계산
    # 'int(input...'과 '*' 연산자가 모두 있는지 확인하여 문제를 감지합니다.
    if re.search(r"[\w\s]*=[\s]*int\(input", src) and re.search(r"\*", src):
        try:
            # 입력값에서 숫자만 추출
            numeric_inputs = [int(line.strip()) for line in stdin_lines if line.strip().isdigit()]
            
            if len(numeric_inputs) >= 1:
                # 숫자 입력값이 1개 이상이면 첫 번째 값을 사용합니다.
                input_value = numeric_inputs[0]
                expected_result = input_value * 2
                
                if re.search(r'\b' + str(expected_result) + r'\b', output):
                    checks.append('✅ 문제 5: 계산 결과가 올바르게 출력되었습니다.')
                else:
                    checks.append('❌ 문제 5: 계산 결과가 올바르지 않거나 출력되지 않았습니다.')
            else:
                checks.append('❌ 문제 5: 계산에 필요한 숫자 입력이 부족합니다.')
        except (ValueError, IndexError):
            checks.append('❌ 문제 5: 입력값 처리 또는 변환 오류')
    else:
        checks.append('❌ 문제 5: 계산 코드가 보이지 않습니다.')

    for c in checks:
        print(c)

    # 채점 결과를 리스트로 반환
    result_lines = list(checks)

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
    # 문제별 결과와 총점 모두 반환
    return {'results': result_lines, 'score': total}
