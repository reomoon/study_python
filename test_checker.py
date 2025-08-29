# 🧪 자동 테스트 파일
# 이 파일은 여러분의 답안을 자동으로 체크합니다.

import importlib.util
import io
import contextlib
import os
import sys
if 'examples' not in sys.path:
    sys.path.append('examples')

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
            print("적당한 주석이 있네요.")
            score += 1
        else:
            print("주석을 조금 더 추가해보세요.")
        
        if meaningful_comments >= 2:
            print("의미 있는 주석들이 잘 작성되어 있어요!")
            score += 1
        elif meaningful_comments >= 1:
            print("의미 있는 주석이 있네요. 좋습니다!")
            score += 1
        else:
            print("📝 간단한 설명 주석을 1-2개 추가해보세요!")
        
        return score
        
    except Exception as e:
        print(f"❌ 주석 검사 중 오류: {e}")
        return 0

def test_week1():
    """Week 1 테스트"""
    # delegate to run_week for consistency with answers/ loader
    return run_week(1)

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

ANSWERS_DIR = os.path.join(os.path.dirname(__file__), 'answers')

def load_answer_modules():
    mods = {}
    if not os.path.isdir(ANSWERS_DIR):
        return mods
    for fn in os.listdir(ANSWERS_DIR):
        if fn.endswith('.py') and not fn.startswith('__'):
            path = os.path.join(ANSWERS_DIR, fn)
            name = f"answers.{fn[:-3]}"
            try:
                spec = importlib.util.spec_from_file_location(name, path)
                m = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(m)
                week = getattr(m, 'WEEK', None)
                if week is not None:
                    mods[int(week)] = m
            except Exception as e:
                print(f"❌ answers 로드 실패: {fn} -> {e}")
    return mods

# 캐시된 answer 모듈 맵
_answer_modules = load_answer_modules()

def run_week(week):
    """주차별 채점 실행기: answers 폴더의 모듈에게 위임합니다."""
    try:
        w = int(week)
    except Exception:
        print("❌ 잘못된 주차 값입니다.")
        return 0

    # reload answer modules if cache doesn't have requested week (helps during development)
    global _answer_modules
    if w not in _answer_modules:
        _answer_modules = load_answer_modules()

    mod = _answer_modules.get(w)
    if not mod:
        print(f"📋 {w}주차 검사가 없습니다.")
        return 0

    # week_module는 app.py가 주입한 메모리 모듈 이름 패턴을 따릅니다
    mem_name = f'week{w}_variable'
    week_module = sys.modules.get(mem_name)
    # 각 answer 모듈은 run(week_module) 함수를 제공해야 함
    import subprocess
    import threading
    import time
    result = {'score': 0, 'error': None}
    def run_with_timeout():
        try:
            result['score'] = mod.run(week_module)
        except Exception as e:
            result['error'] = str(e)

    t = threading.Thread(target=run_with_timeout)
    t.start()
    t.join(timeout=2)  # 2초 제한
    if t.is_alive():
        print(f"⏰ 실행이 너무 오래 걸립니다. 무한루프나 입력 대기 상태일 수 있습니다.")
        return 0
    if result['error']:
        print(f"❌ {w}주차 검사 실행 중 오류: {result['error']}")
        return 0
    return result['score']

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
