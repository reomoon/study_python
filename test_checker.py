# 🧪 자동 테스트 파일
# 이 파일은 여러분의 답안을 자동으로 체크합니다.

import importlib.util
import sys
import io
import contextlib
import os

def check_comments(filename):
    """주석 품질을 검사하는 함수"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        comment_lines = 0
        code_lines = 0
        meaningful_comments = 0
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('#'):
                comment_lines += 1
                # 의미 있는 주석인지 확인 (기본 템플릿이 아닌)
                if (stripped != '#' and 
                    '답을 아래에 작성하세요' not in stripped and
                    '문제' not in stripped and
                    len(stripped) > 10):
                    meaningful_comments += 1
            elif stripped and not stripped.startswith('#'):
                code_lines += 1
        
        comment_ratio = (comment_lines * 100 // code_lines) if code_lines > 0 else 0
        
        print(f"📊 주석 통계:")
        print(f"   - 전체 라인: {total_lines}")
        print(f"   - 주석 라인: {comment_lines}")
        print(f"   - 코드 라인: {code_lines}")
        print(f"   - 주석 비율: {comment_ratio}%")
        print(f"   - 의미있는 주석: {meaningful_comments}개")
        
        score = 0
        if comment_ratio >= 15:
            print("✅ 주석이 충분합니다!")
            score += 2
        elif comment_ratio >= 8:
            print("👍 적당한 주석이 있네요.")
            score += 1
        else:
            print("💡 주석을 조금 더 추가해보세요.")
        
        if meaningful_comments >= 2:
            print("✨ 의미 있는 주석들이 잘 작성되어 있어요!")
            score += 1
        elif meaningful_comments >= 1:
            print("💡 의미 있는 주석이 있네요. 좋습니다!")
            score += 1
        else:
            print("📝 간단한 설명 주석을 1-2개 추가해보세요!")
        
        return score
        
    except Exception as e:
        print(f"❌ 주석 검사 중 오류: {e}")
        return 0

def test_week1():
    """Week 1 테스트"""
    print("📝 Week 1 테스트 시작...")
    
    try:
        # 우선 메모리 모듈로 주입된 `week1_variable` 확인 (Vercel 등 읽기전용 FS 대응)
        if 'week1_variable' in sys.modules:
            week1 = sys.modules['week1_variable']
            # 메모리 모듈이 원본 코드를 가지고 있으면 그 소스에서 출력 캡처
            src = getattr(week1, '__source__', None)
            if src is not None:
                f = io.StringIO()
                with contextlib.redirect_stdout(f):
                    # 실행은 이미 되었을 수 있으니 재실행하여 출력 캡처
                    exec(src, week1.__dict__)
                output = f.getvalue()
            else:
                output = ''
        else:
            # 파일 기반 로딩 (로컬 개발 환경)
            spec = importlib.util.spec_from_file_location("week1", "week1_variable.py")
            week1 = importlib.util.module_from_spec(spec)
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                spec.loader.exec_module(week1)
            output = f.getvalue()
        
        # 기본 체크 항목들
        checks = []
        
        # 변수 x가 정의되어 있는지 확인
        if hasattr(week1, 'x') and week1.x == 7:
            checks.append("✅ 문제 1: 변수 x 정의 완료")
        else:
            checks.append("❌ 문제 1: 변수 x가 7로 설정되지 않았습니다")
        
        # 출력에 필요한 내용이 포함되어 있는지 확인
        if "x는" in output and "7" in output:
            checks.append("✅ 문제 1: 출력 형식 올바름")
        else:
            checks.append("❌ 문제 1: 출력 형식을 확인해주세요")
        
        for check in checks:
            print(check)
        
        # 주석 품질 검사 추가 (메모리 모듈의 소스가 있으면 그 소스를 검사)
        print("\n💬 주석 품질 검사:")
        if 'week1_variable' in sys.modules and getattr(sys.modules['week1_variable'], '__source__', None):
            # 메모리 모듈의 소스에서 줄 리스트를 만들고 통계 산출
            src = sys.modules['week1_variable'].__source__
            # 임시로 파일에 쓰지 않고 문자열에서 검사를 수행
            lines = src.splitlines()
            # write a temporary helper to reuse check_comments logic: create a temp file-like handling
            # For simplicity, we'll write lines to a temp file only in local dev; here we'll mimic
            with open('._tmp_week1_source.txt', 'w', encoding='utf-8') as tf:
                tf.write('\n'.join(lines))
            comment_score = check_comments('._tmp_week1_source.txt')
            try:
                os.remove('._tmp_week1_source.txt')
            except Exception:
                pass
        else:
            comment_score = check_comments('week1_variable.py')
        
        total_score = len([c for c in checks if c.startswith("✅")]) + comment_score
        return total_score
        
    except Exception as e:
        print(f"❌ Week 1 테스트 실행 중 오류: {e}")
        return 0

def test_week2():
    """Week 2 테스트"""
    print("\n📝 Week 2 테스트 시작...")
    
    try:
        # week2_datatype.py 파일 체크
        with open("week2_datatype.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        checks = []
        
        # 주석이 제거되고 실제 코드가 작성되었는지 확인
        if "type(" in content and "num = 42" in content.replace("#", "").replace(" ", ""):
            checks.append("✅ 문제 1: 타입 확인 코드 작성됨")
        else:
            checks.append("❌ 문제 1: 타입 확인 코드를 작성해주세요")
        
        if "a = 15" in content.replace("#", "").replace(" ", "") and "b = 4" in content.replace("#", "").replace(" ", ""):
            checks.append("✅ 문제 2: 사칙연산 변수 설정됨")
        else:
            checks.append("❌ 문제 2: 사칙연산 변수를 설정해주세요")
        
        for check in checks:
            print(check)
        
        # 주석 품질 검사 추가
        print("\n💬 주석 품질 검사:")
        comment_score = check_comments("week2_datatype.py")
        
        total_score = len([c for c in checks if c.startswith("✅")]) + comment_score
        return total_score
        
    except FileNotFoundError:
        print("❌ week2_datatype.py 파일을 찾을 수 없습니다")
        return 0
    except Exception as e:
        print(f"❌ Week 2 테스트 실행 중 오류: {e}")
        return 0

def main():
    """메인 테스트 함수"""
    print("🤖 AI 선생님의 자동 테스트를 시작합니다!")
    print("=" * 60)
    
    total_score = 0
    max_score = 0
    
    # Week 1 테스트
    week1_score = test_week1()
    total_score += week1_score
    max_score += 5  # Week 1 최대 점수 (코드 2점 + 주석 3점)
    
    # Week 2 테스트 (파일이 있는 경우에만)
    try:
        with open("week2_datatype.py", "r"):
            week2_score = test_week2()
            total_score += week2_score
            max_score += 5  # Week 2 최대 점수 (코드 2점 + 주석 3점)
    except FileNotFoundError:
        print("\n📋 Week 2는 아직 시작하지 않으셨군요!")
    
    # 결과 출력
    print("\n" + "=" * 60)
    print(f"📊 총 점수: {total_score}/{max_score}")
    
    if total_score == max_score:
        print("🏆 완벽합니다! 모든 문제를 올바르게 해결하고 주석도 훌륭해요!")
    elif total_score >= max_score * 0.8:
        print("👍 잘 했어요! 몇 가지만 더 수정하면 완벽할 것 같아요!")
    elif total_score >= max_score * 0.6:
        print("🌟 좋은 시작이에요! 주석을 더 추가하고 조금 더 화이팅하세요!")
    else:
        print("💪 아직 갈 길이 있지만 포기하지 마세요! 코드와 주석을 차근차근 작성해보세요!")
    
    # 주석 작성 팁 제공
    print("\n💡 주석 작성 팁:")
    print("- 각 변수가 무엇을 저장하는지 설명해보세요")
    print("- 계산 과정을 단계별로 설명해보세요")  
    print("- 출력 결과가 무엇을 의미하는지 적어보세요")
    print("- 예: # 사각형의 가로 길이를 저장")
    print("- 예: # 가로 × 세로로 넓이를 계산")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
