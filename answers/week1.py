WEEK = 1

def _compute_comment_score_from_source(src_lines):
    total_lines = len(src_lines)
    comment_lines = 0
    code_lines = 0
    meaningful_comments = 0
    for line in src_lines:
        stripped = line.strip()
        if stripped.startswith('#'):
            comment_lines += 1
            if (stripped != '#' and '답을 아래에 작성하세요' not in stripped and '문제' not in stripped and len(stripped) > 10):
                meaningful_comments += 1
        elif stripped and not stripped.startswith('#'):
            code_lines += 1

    comment_ratio = (comment_lines * 100 // code_lines) if code_lines > 0 else 0
    score = 0
    if comment_ratio >= 15:
        score += 2
    elif comment_ratio >= 8:
        score += 1
    if meaningful_comments >= 1:
        score += 1
    return score

def run(week_module):
    """Run week1 checks. week_module may be an in-memory module injected by app.py."""
    import importlib.util, sys, io, contextlib, os

    # Load week module (memory preferred)
    output = ''
    week1 = None
    if week_module is not None:
        week1 = week_module
        src = getattr(week1, '__source__', None)
        if src is not None:
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                try:
                    exec(src, week1.__dict__)
                except Exception as e:
                    print(f"❌ 코드 실행 중 오류: {e}")
            output = f.getvalue()
    if week1 is None:
        # try file fallback
        try:
            spec = importlib.util.spec_from_file_location("week1", "week1_variable.py")
            week1 = importlib.util.module_from_spec(spec)
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                spec.loader.exec_module(week1)
            output = f.getvalue()
        except Exception:
            week1 = None

    checks = []
    # 1
    if week1 is not None and hasattr(week1, 'x') and week1.x == 7:
        checks.append("✅ 문제 1: 변수 x 정의 완료")
    else:
        checks.append("❌ 문제 1: 변수 x가 7로 설정되지 않았습니다")
    if "x는" in output and "7" in output:
        checks.append("✅ 문제 1 출력: 출력 형식 올바름")
    else:
        checks.append("❌ 문제 1 출력: 출력 형식을 확인해주세요")

    # 2
    if week1 is not None and hasattr(week1, 'a') and hasattr(week1, 'b') and (week1.a * week1.b == 3 * 8):
        checks.append("✅ 문제 2: 변수 a,b 정의 및 곱 계산 완료")
    else:
        checks.append("❌ 문제 2: 변수 a,b가 없거나 곱이 올바르지 않습니다")
    if "24" in output:
        checks.append("✅ 문제 2 출력: 곱 출력 확인")
    else:
        checks.append("❌ 문제 2 출력: 곱 결과가 출력되지 않았습니다")

    # 3
    if week1 is not None and hasattr(week1, 'name') and isinstance(getattr(week1, 'name'), str):
        checks.append("✅ 문제 3: name 변수 정의 완료")
    else:
        checks.append("❌ 문제 3: name 변수가 정의되지 않았습니다")
    if "내 이름은" in output:
        checks.append("✅ 문제 3 출력: 이름 출력 형식 확인")
    else:
        checks.append("❌ 문제 3 출력: 이름 출력이 형식에 맞지 않습니다")

    # 4
    if week1 is not None and hasattr(week1, 'width') and hasattr(week1, 'height') and (getattr(week1, 'width') * getattr(week1, 'height') == 5 * 10):
        checks.append("✅ 문제 4: width,height 정의 및 넓이 계산 완료")
    else:
        checks.append("❌ 문제 4: width/height가 없거나 넓이 계산이 올바르지 않습니다")
    if "50" in output:
        checks.append("✅ 문제 4 출력: 넓이 출력 확인")
    else:
        checks.append("❌ 문제 4 출력: 넓이 결과가 출력되지 않았습니다")

    # 5
    if week1 is not None and hasattr(week1, 'temp') and (getattr(week1, 'temp') == 36.5):
        checks.append("✅ 문제 5: temp 변수 정의 완료")
    else:
        checks.append("❌ 문제 5: temp 변수가 없거나 값이 올바르지 않습니다")
    if "현재 체온" in output and "36.5" in output:
        checks.append("✅ 문제 5 출력: 체온 출력 형식 확인")
    else:
        checks.append("❌ 문제 5 출력: 체온 출력이 형식에 맞지 않습니다")

    for c in checks:
        print(c)

    # comment score
    comment_score = 0
    src_lines = None
    if week1 is not None and getattr(week1, '__source__', None):
        src_lines = week1.__source__.splitlines()
    else:
        try:
            with open('week1_variable.py', 'r', encoding='utf-8') as f:
                src_lines = f.read().splitlines()
        except Exception:
            src_lines = []
    comment_score = _compute_comment_score_from_source(src_lines)
    print("\n💬 주석 품질 검사:")
    print(f"   - 주석 점수: {comment_score}")

    total_score = len([c for c in checks if c.startswith("✅")]) + comment_score
    return total_score
WEEK = 1

import io
import contextlib

def run(week_module):
    """Week1 검사기: week_module은 app에서 주입한 메모리 모듈 또는 None.
    출력은 print로 남기고, 최종 점수(int)를 반환합니다.
    """
    print("📝 Week 1 검사기 실행...")
    try:
        # 출력 캡처
        output = ''
        if week_module is not None:
            src = getattr(week_module, '__source__', None)
            if src is not None:
                f = io.StringIO()
                with contextlib.redirect_stdout(f):
                    # 재실행하여 출력 캡처
                    exec(src, week_module.__dict__)
                output = f.getvalue()
            else:
                # 이미 실행되어 있을 경우, 빈 출력 처리
                output = ''
        else:
            # file-based loading is handled by caller if needed
            output = ''

        checks = []

        # 1) x
        if week_module and hasattr(week_module, 'x') and week_module.x == 7:
            checks.append("✅ 문제 1: 변수 x 정의 완료")
        else:
            checks.append("❌ 문제 1: 변수 x가 7로 설정되지 않았습니다")
        if "x는" in output and "7" in output:
            checks.append("✅ 문제 1 출력: 출력 형식 올바름")
        else:
            checks.append("❌ 문제 1 출력: 출력 형식을 확인해주세요")

        # 2) a,b 곱
        if week_module and hasattr(week_module, 'a') and hasattr(week_module, 'b') and (week_module.a * week_module.b == 24):
            checks.append("✅ 문제 2: 변수 a,b 정의 및 곱 계산 완료")
        else:
            checks.append("❌ 문제 2: 변수 a,b가 없거나 곱이 올바르지 않습니다")
        if "24" in output:
            checks.append("✅ 문제 2 출력: 곱 출력 확인")
        else:
            checks.append("❌ 문제 2 출력: 곱 결과가 출력되지 않았습니다")

        # 3) name
        if week_module and hasattr(week_module, 'name') and isinstance(getattr(week_module, 'name'), str):
            checks.append("✅ 문제 3: name 변수 정의 완료")
        else:
            checks.append("❌ 문제 3: name 변수가 정의되지 않았습니다")
        if "내 이름은" in output:
            checks.append("✅ 문제 3 출력: 이름 출력 형식 확인")
        else:
            checks.append("❌ 문제 3 출력: 이름 출력이 형식에 맞지 않습니다")

        # 4) width,height 넓이
        if week_module and hasattr(week_module, 'width') and hasattr(week_module, 'height') and (getattr(week_module, 'width') * getattr(week_module, 'height') == 50):
            checks.append("✅ 문제 4: width,height 정의 및 넓이 계산 완료")
        else:
            checks.append("❌ 문제 4: width/height가 없거나 넓이 계산이 올바르지 않습니다")
        if "50" in output:
            checks.append("✅ 문제 4 출력: 넓이 출력 확인")
        else:
            checks.append("❌ 문제 4 출력: 넓이 결과가 출력되지 않았습니다")

        # 5) temp
        if week_module and hasattr(week_module, 'temp') and (getattr(week_module, 'temp') == 36.5):
            checks.append("✅ 문제 5: temp 변수 정의 완료")
        else:
            checks.append("❌ 문제 5: temp 변수가 없거나 값이 올바르지 않습니다")
        if "현재 체온" in output and "36.5" in output:
            checks.append("✅ 문제 5 출력: 체온 출력 형식 확인")
        else:
            checks.append("❌ 문제 5 출력: 체온 출력이 형식에 맞지 않습니다")

        for c in checks:
            print(c)

        # 단순 점수: 체크된 ✅의 개수
        score = len([c for c in checks if c.startswith("✅")])
        return score

    except Exception as e:
        print("❌ Week1 검사기 실행 중 오류:", e)
        return 0
