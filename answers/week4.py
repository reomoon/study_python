"""
정규식에서 사용되는 주요 패턴 설명:
    - \s+ : 하나 이상의 공백 문자 (space, tab 등)
    - \w+ : 하나 이상의 영문자, 숫자, 밑줄(변수명에 해당)
예시: r"if\s+\w+\s*>\s*10"은 'if' 다음에 변수명, 그 뒤에 '>'와 10이 있는 조건문을 찾음
"""
import io, contextlib, importlib.util, re

def grade_week4(module_path):
    spec = importlib.util.spec_from_file_location('week4', module_path)
    mod = importlib.util.module_from_spec(spec)
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        spec.loader.exec_module(mod)
    output = f.getvalue()
    checks = []

    # 1. 짝수/홀수 판별
    if re.search(r"짝수|홀수", output):
        checks.append('✅ 문제 1: 짝수/홀수 판별 출력')
    else:
        checks.append('❌ 문제 1: 짝수/홀수 판별 없음')

    # 2. 영/음수/양수 판별
    print("지나갑니다")
    if re.search(r"영|음수|양수", output, re.IGNORECASE):
        print("지나갑니다")
        checks.append('✅ 문제 2: 영/음수/양수 모두 출력 확인')
    else:
        print("지나갑니다")
        checks.append('❌ 문제 2: 영/음수/양수 출력 누락')

    # 3. 입력 오류 예외처리
    if re.search(r"입력 오류", output):
        checks.append('✅ 문제 3: 입력 오류 예외처리')
    else:
        checks.append('❌ 문제 3: 입력 오류 예외처리 없음')

    # 4. 10보다 큰지 확인
    if re.search(r"10보다 큽니다|10보다 작습니다|10 입니다", output):
        checks.append('✅ 문제 4: 10 비교 출력')
    else:
        checks.append('❌ 문제 4: 10 비교 출력 없음')

    # 5. 강제 에러 및 예외처리
    if re.search(r"에러 잡음", output):
        checks.append('✅ 문제 5: 강제 에러 예외처리')
    else:
        checks.append('❌ 문제 5: 강제 에러 예외처리 없음')

    for c in checks:
        print(c)

    return sum(c.startswith('✅') for c in checks)

WEEK = 4

def run(week_module, student_output, stdin_text):
    import io, contextlib, importlib.util, inspect

    module = week_module
    output = ''
    src = ''

    # --- normalize: test_checker가 리스트로 보내는 경우 대비 ---
    if isinstance(student_output, list):
        student_output = "\n".join(student_output)
    if isinstance(stdin_text, list):
        stdin_text = "\n".join(stdin_text)

    # --- 경우 1: app.py가 이미 실행해서 module.__source__에 소스가 들어있다면
    if module is not None and getattr(module, '__source__', None):
        src = getattr(module, '__source__', '')
        # 이미 캡처된 실행 출력이 있다면(앱이 실행하여 전달) 그 값을 우선 사용
        if student_output:
            output = student_output
        else:
            # fallback: 소스를 다시 실행해야 하는 경우에만 stdin을 제공해서 실행
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                try:
                    # contextlib.redirect_stdin이 있으면 사용하여 stdin_text 제공
                    if hasattr(contextlib, 'redirect_stdin'):
                        from io import StringIO
                        with contextlib.redirect_stdin(StringIO(stdin_text or '')):
                            exec(src, module.__dict__)
                    else:
                        # 최소한의 안전 실행: input()호출 시 EOFError 처리 유도
                        exec(src, module.__dict__)
                except Exception as e:
                    # 실행 오류는 출력으로 남김
                    print(f"❌ 코드 실행 오류: {e}")
            output = f.getvalue()

    else:
        # --- 경우 2: 메모리 모듈이 없으면 파일에서 예제/조건 파일을 로드 ---
        try:
            spec = importlib.util.spec_from_file_location('week4', 'week4_condition.py')
            mod = importlib.util.module_from_spec(spec)
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                spec.loader.exec_module(mod)
            output = f.getvalue()
            module = mod
            try:
                src = inspect.getsource(mod)
            except Exception:
                src = ''
        except Exception:
            module = None

        if module is None:
            try:
                spec = importlib.util.spec_from_file_location('week4', 'examples/week4_example.py')
                mod = importlib.util.module_from_spec(spec)
                f = io.StringIO()
                with contextlib.redirect_stdout(f):
                    spec.loader.exec_module(mod)
                output = f.getvalue()
                module = mod
                try:
                    src = inspect.getsource(mod)
                except Exception:
                    src = ''
            except Exception:
                module = None

    # --- 채점 로직: 이제 'output' 문자열과 'src' 문자열만 사용 ---
    import re
    checks = []

    # 1) 짝수/홀수 관련 출력
    if re.search(r"짝|홀", output, re.IGNORECASE):
        checks.append('✅ 문제 1: 짝수/홀수 판별 출력 확인')
    else:
        checks.append('❌ 문제 1: 짝수/홀수 출력이 보이지 않습니다')

    # 2) 영/음수/양수 관련 출력
    if re.search(r"영|음수|양수", output, re.IGNORECASE):
        checks.append('✅ 문제 2: 영/음수/양수 모두 출력 확인')
    else:
        checks.append('❌ 문제 2: 영/음수/양수 출력 누락')

    # 3) 예외 처리 출력 확인
    if re.search(r"입력 오류|ValueError|예외|오류|에러", output, re.IGNORECASE):
        checks.append('✅ 문제 3: 예외 처리 출력 확인')
    else:
        checks.append('❌ 문제 3: 예외 처리 코드 또는 출력이 보이지 않습니다')

    # 4) 10 비교: 소스가 있으면 소스에서 if/elif 패턴 검사, 없으면 출력 문구로 대체검사
    src_to_check = src or ''
    if src_to_check and (re.search(r"if\s+\w+\s*>\s*10", src_to_check) or re.search(r"elif\s+\w+\s*<\s*10", src_to_check)):
        checks.append('✅ 문제 4: 10 비교 조건문 확인')
    else:
        # 소스가 없을 때는 출력 문구로 검사 (학생 출력에 '10보다 큽니다' 등 표현이 있는지)
        if re.search(r"10보다 큽니다|10보다 작습니다|10 입니다", output):
            checks.append('✅ 문제 4: 10 비교 출력 확인')
        else:
            checks.append('❌ 문제 4: 10 비교 조건문 없음')

    # 5) 에러/예외 관련 출력 확인
    if re.search(r"에러|Exception|오류|예외", output, re.IGNORECASE):
        checks.append('✅ 문제 5: 에러 발생/처리 출력 확인')
    else:
        checks.append('❌ 문제 5: 에러 처리 출력이 보이지 않습니다')

    # 출력된 체크 결과
    for c in checks:
        print(c)

    # 주석 히스테리틱(원래 로직 유지)
    try:
        if module is not None and getattr(module, '__source__', None):
            lines = module.__source__.splitlines()
        else:
            with open('week4_condition.py','r',encoding='utf-8') as f:
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
