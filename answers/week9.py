"""
이 파일의 채점 기준은 정규표현식(정규식, Regular Expression)을 사용하여
학생 코드(src)에서 각 항목별로 필요한 코드 패턴이 실제로 들어가 있는지 검사합니다.

예시:
    - 파일명 변수 선언:   r"fn\s*=\s*['\"][^\"]*\.txt['\"]"
    - 파일 쓰기:         r"with\s+open\s*\(fn\s*,\s*['\"]w['\"]"
    - 파일 읽기:         r"with\s+open\s*\(fn\s*,\s*['\"]r['\"]"
    - 예외 처리:         r"except\s+FileNotFoundError"
    - 파일 삭제:         r"os\.remove\s*\(fn\s*\)"

정규식은 파이썬 re 모듈로 사용하며, re.search(패턴, 코드)로 검사합니다.
각 항목별로 코드가 실제로 들어가 있으면 ✅, 없으면 ❌로 채점됩니다.
"""

def static_analysis(src):
    import re
    checks = []

     # 0번: 파일명 변수 선언 (fn = '*.txt')
    if re.search(r"fn\s*=\s*['\"]\w+\.txt['\"]", src):
        checks.append('✅ 문제 0: 파일명 변수 선언 확인')
    else:
        checks.append('❌ 문제 0: 파일명 변수 선언이 없습니다')


    # 1번: 파일 쓰기 (with open(..., 'w'), f.write)
    if re.search(r"with\s+open\s*\(.*['\"]w['\"].*\)", src, re.I) and re.search(r"\.write\s*\(", src):
        checks.append('✅ 문제 1: 파일 쓰기 코드 확인')
    else:
        checks.append('❌ 문제 1: 파일 쓰기 코드가 없습니다')

    # 2번: 파일 읽기 (with open(..., 'r'), f.read)
    pattern_with_open = r"with\s+open\s*\(\s*fn\s*,\s*['\"]r['\"].*?\)\s*as\s+f\s*:"
    pattern_f_read = r"content\s*=\s*f\.read\s*\("
    pattern_print_content = r"print\s*\(\s*content\s*\)"

    if (re.search(pattern_with_open, src, re.I | re.S) and
        re.search(pattern_f_read, src, re.I | re.S) and
        re.search(pattern_print_content, src, re.I | re.S)):
        checks.append('✅ 문제 2: 파일 읽기 코드 확인')
    else:
        checks.append('❌ 문제 2: 파일 읽기 코드가 없습니다')

    # 3번: 예외 처리 (with open(..., 'r'), except FileNotFoundError)
    pattern3 = r"except\s+FileNotFoundError"
    if re.search(pattern3, src):
        checks.append('✅ 문제 3: 파일 예외 처리 코드 확인')
    else:
        checks.append('❌ 문제 3: 파일 예외 처리 코드가 없습니다')

    # 4번: 파일 읽고 print로 변수 출력 (with open(..., 'r'), print())
    pattern_with_open = r"with\s+open\s*\(\s*fn\s*,\s*['\"]r['\"].*?\)"
    pattern_readlines = r"lines\s*=\s*f\.readlines\s*\("
    pattern_print_lines = r"print\s*\(\s*lines\s*\)"
    pattern_print_len = r"print\s*\(\s*len\s*\(\s*lines\s*\)\s*\)"

    # re.DOTALL을 써서 여러 줄에 걸쳐 있어도 검색 가능하게
    if (re.search(pattern_with_open, src, re.I | re.DOTALL) and
        re.search(pattern_readlines, src, re.I | re.DOTALL) and
        re.search(pattern_print_lines, src, re.I | re.DOTALL) and
        re.search(pattern_print_len, src, re.I | re.DOTALL)):
        checks.append('✅ 문제 4: 파일 읽고 변수 출력 코드 확인')
    else:
        checks.append('❌ 문제 4: 파일 읽고 변수 출력 코드가 없습니다')

    # 5번: 파일 append (with open(..., 'a'), f.write)
    if re.search(r"with\s+open\s*\(.*['\"]a['\"].*\)", src, re.I) and re.search(r"\.write\s*\(", src):
        checks.append('✅ 문제 5: 파일 append 코드 확인')
    else:
        checks.append('❌ 문제 5: 파일 append 코드가 없습니다')

    # 6번: 파일 삭제 (os.remove(fn))
    if re.search(r"os\.remove\s*\(fn\s*\)", src):
        checks.append('✅ 문제 6: 파일 삭제 코드 확인')
    else:
        checks.append('❌ 문제 6: 파일 삭제 코드가 없습니다')

    return checks

def comment_score(lines):
    comment_lines = sum(1 for l in lines if l.strip().startswith('#'))
    code_lines = sum(1 for l in lines if l.strip() and not l.strip().startswith('#'))
    score = 0
    if code_lines > 0:
        ratio = comment_lines * 100 // code_lines
        if ratio >= 15:
            score = 2
        elif ratio >= 8:
            score = 1
    return score

def check_code(code):
    result = "==== 제출 코드 ====" + "\n" + code + "\n" + "===================\n"
    checks = static_analysis(code)
    lines = code.splitlines()
    c_score = comment_score(lines)
    total = len([c for c in checks if c.startswith('✅')]) + c_score
    result = '\n'.join(checks)
    result += f"\n코멘트 점수: {c_score}"
    result += f"\n총점: {total}"
    return result
WEEK = 9

def run(week_module):
    import io, contextlib, importlib.util, os

    module = week_module
    output = ''
    if module is not None and getattr(module, '__source__', None):
        src = module.__source__
        # 파일 입출력 환경 문제 방지: 실제 실행하지 않고 코드만 검사
        output = ''
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
        if module is None:
            try:
                spec = importlib.util.spec_from_file_location('week9', 'examples/week9_example.py')
                mod = importlib.util.module_from_spec(spec)
                f = io.StringIO()
                with contextlib.redirect_stdout(f):
                    spec.loader.exec_module(mod)
                output = f.getvalue()
                module = mod
            except Exception:
                module = None

    src = module.__source__ if module and getattr(module,'__source__',None) else ''
    checks = static_analysis(src)
    for c in checks:
        print(c)
    try:
        if src:
            lines = src.splitlines()
        else:
            with open('week9_fileio.py','r',encoding='utf-8') as f:
                lines = f.read().splitlines()
    except Exception:
        lines = []
    c_score = comment_score(lines)
    total = len([c for c in checks if c.startswith('✅')]) + c_score
    return total
