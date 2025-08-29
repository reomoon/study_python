def static_analysis(src):
    import re
    checks = []
    # 파일명 변수 선언만 있어도 인정
    if re.search(r"fn\s*=\s*['\"]examples_week9.txt['\"]", src):
        checks.append('✅ 문제 0: 파일명 변수 선언 확인')

    if re.search(r"\bopen\s*\(|with\s+open\s*\(", src):
        checks.append('✅ 문제 1/2: 파일 열기/쓰기/읽기 사용 감지')
    else:
        checks.append('❌ 문제 1/2: 파일 입출력 코드가 보이지 않습니다')

    if re.search(r"\bexcept\b", src):
        checks.append('✅ 문제 3: 예외 처리 코드 감지')
    else:
        checks.append('❌ 문제 3: 파일 예외 처리 코드가 보이지 않습니다')

    if re.search(r"read\b|readlines\b|len\b", src):
        checks.append('✅ 문제 4: 파일 읽기/길이 출력 코드 감지')
    else:
        checks.append('❌ 문제 4: 파일 읽기/길이 출력 코드가 보이지 않습니다')

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
