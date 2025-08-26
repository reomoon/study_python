#!/usr/bin/env python3
"""
간단한 채점기 테스트 하니스
- answers 폴더의 weekN.py 채점기를 찾아서
  examples 폴더의 예제(weekN_example.py)를 불러와 메모리 모듈로 실행
- 채점기 출력과 실행 결과를 캡처하여 한국어 혼합형 문구로 리포트

사용: python run_grader_tests.py
"""
import os
import re
import sys
import io
import types
import importlib
import traceback
from contextlib import redirect_stdout


def find_answer_files(path='answers'):
    if not os.path.isdir(path):
        return []
    files = []
    for name in os.listdir(path):
        m = re.match(r'^week(\d+)\.py$', name)
        if m:
            files.append((int(m.group(1)), name))
    return sorted(files)


def find_example_for_week(week, examples_dir='examples'):
    if not os.path.isdir(examples_dir):
        return None
    candidates = [
        f'week{week}_example.py',
        f'week{week}.py',
        f'week{week}_example.txt',
    ]
    for c in candidates:
        p = os.path.join(examples_dir, c)
        if os.path.isfile(p):
            return p
    # fallback: any file starting with week{n}
    for name in os.listdir(examples_dir):
        if name.startswith(f'week{week}'):
            return os.path.join(examples_dir, name)
    return None


def friendly_summary(score, exc, grader_out, student_out):
    # 혼합형 스타일: 친절한 총괄 + 기술적 세부
    if exc is not None:
        return ('실행 중 오류 발생 — 제출 코드 또는 채점기에서 예외가 발생했습니다.', 'error')
    if score is None:
        # 채점기가 정수 점수를 반환하지 않는 경우, 출력 기반 판단
        if '✅' in grader_out:
            return ('완료: 일부 항목이 통과되었습니다. 세부 항목을 확인하세요.', 'partial')
        else:
            return ('검토 필요: 채점 결과가 기대와 다릅니다.', 'fail')
    # 정수 점수 판정
    try:
        s = int(score)
    except Exception:
        return ('검토 필요: 채점기가 비정상적인 점수를 반환했습니다.', 'fail')
    if s >= 90:
        return ('좋습니다 — 기대한 결과가 거의 일치하거나 완전히 일치합니다.', 'pass')
    if s >= 60:
        return ('거의 맞았습니다 — 몇 가지 항목만 추가 확인이 필요합니다.', 'partial')
    return ('다시 확인해 보세요 — 출력이나 구현이 요구사항과 다릅니다.', 'fail')


def run_one(week, example_path):
    # 읽기
    src = open(example_path, 'r', encoding='utf-8').read()

    # 학생 모듈처럼 메모리 모듈 생성
    modname = f'week{week}_variable'
    module = types.ModuleType(modname)
    module.__source__ = src
    sys.modules[modname] = module

    student_out = ''
    exc = None
    # 실행(학생 코드)
    try:
        buf = io.StringIO()
        # 자동 입력 감지: 소스에 input( 호출이 있으면 기본값을 주입
        input_calls = list(re.finditer(r"input\s*\(", src))
        stdin_lines = []
        if input_calls:
            # 간단 휴리스틱: input 앞에 int( 가 있으면 숫자 예제(3), 아니면 이름 '홍길동'
            for m in input_calls:
                start = max(0, m.start()-10)
                context = src[start:m.start()]
                if 'int' in context:
                    stdin_lines.append('3')
                else:
                    stdin_lines.append('홍길동')

        class RedirectInput:
            def __init__(self, lines):
                self.lines = list(lines)
                self._orig = None
            def __enter__(self):
                import builtins
                self._orig = builtins.input
                def _input(prompt=None):
                    if self.lines:
                        return self.lines.pop(0)
                    raise EOFError('No more input')
                builtins.input = _input
                return self
            def __exit__(self, exc_type, exc, tb):
                import builtins
                builtins.input = self._orig

        with redirect_stdout(buf):
            try:
                if stdin_lines:
                    with RedirectInput(stdin_lines):
                        exec(src, module.__dict__)
                else:
                    exec(src, module.__dict__)
            except Exception:
                exc = traceback.format_exc()
        student_out = buf.getvalue()
    except Exception as e:
        exc = traceback.format_exc()

    # 채점기 임포트 및 실행
    grader_out = ''
    score = None
    try:
        grader_mod = importlib.import_module(f'answers.week{week}')
        # reload to pick up edits
        importlib.reload(grader_mod)
        buf = io.StringIO()
        with redirect_stdout(buf):
            try:
                score = grader_mod.run(module)
            except TypeError:
                # 일부 채점기는 run()를 인자로 안받는 경우가 있을 수 있으므로 시도
                try:
                    score = grader_mod.run()
                except Exception:
                    raise
        grader_out = buf.getvalue()
    except Exception:
        grader_out = traceback.format_exc()
        if exc is None:
            # 마찬가지로 실행 에러로 간주
            exc = None

    return score, exc, grader_out, student_out


def print_report(week, example_path, score, exc, grader_out, student_out):
    title = f'== 주차 {week} 결과 =='
    print(title)
    print('-' * len(title))
    summary, status = friendly_summary(score, exc, grader_out, student_out)
    print('요약:', summary)
    # 기술적 세부
    if score is not None:
        print('점수(채점기 반환값):', score)
    if exc is not None:
        print('\n[예외 스택트레이스]\n')
        print(exc)
    print('\n[채점기 출력]\n')
    print(grader_out.strip() or '(없음)')
    print('\n[학생 코드 출력]\n')
    print(student_out.strip() or '(없음)')
    print('\n[사용된 예제 파일]', example_path)
    print('\n')


def main():
    answers = find_answer_files('answers')
    if not answers:
        print('answers 폴더에서 채점기를 찾을 수 없습니다.')
        return

    total = {'pass': 0, 'partial': 0, 'fail': 0, 'error': 0}
    for week, filename in answers:
        example = find_example_for_week(week, 'examples')
        if not example:
            print(f'주차 {week}: 예제 파일이 없습니다. (스킵)')
            continue
        score, exc, grader_out, student_out = run_one(week, example)
        summary, status = friendly_summary(score, exc, grader_out, student_out)
        if status in total:
            total[status] += 1
        else:
            total['fail'] += 1
        print_report(week, example, score, exc, grader_out, student_out)

    print('요약: 총 검사 결과')
    for k, v in total.items():
        print(f'  {k}: {v}')


if __name__ == '__main__':
    main()
