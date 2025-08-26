WEEK = 10

def run(week_module):
    import io, contextlib, importlib.util

    module = week_module
    output = ''
    if module is not None and getattr(module, '__source__', None):
        src = module.__source__
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            try:
                exec(src, module.__dict__)
            except Exception as e:
                print(f"❌ 코드 실행 오류: {e}")
        output = f.getvalue()
    else:
        try:
            spec = importlib.util.spec_from_file_location('week10', 'week10_class.py')
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
                spec = importlib.util.spec_from_file_location('week10', 'examples/week10_example.py')
                mod = importlib.util.module_from_spec(spec)
                f = io.StringIO()
                with contextlib.redirect_stdout(f):
                    spec.loader.exec_module(mod)
                output = f.getvalue()
                module = mod
            except Exception:
                module = None

    checks = []
    # Person class
    person_cls = None
    if module is not None:
        person_cls = module.__dict__.get('Person')
    if person_cls:
        checks.append('✅ 문제 1: Person 클래스 정의 확인')
    else:
        checks.append('❌ 문제 1: Person 클래스가 정의되지 않았습니다')

    # greet method
    if person_cls and hasattr(person_cls, 'greet'):
        checks.append('✅ 문제 2: greet 메서드 존재 확인')
    else:
        checks.append('❌ 문제 2: greet 메서드가 없습니다')

    # instance usage
    import re
    if re.search(r"안녕하세요|제 이름", output):
        checks.append('✅ 문제 3: 인스턴스 생성 및 메서드 호출 출력 확인')
    else:
        checks.append('❌ 문제 3: 인스턴스 출력이 보이지 않습니다')

    # inheritance Student
    if module is not None and 'Student' in module.__dict__:
        checks.append('✅ 문제 4: Student 상속 클래스 확인')
    else:
        checks.append('❌ 문제 4: Student 클래스가 없습니다')

    # __str__ or __repr__
    src = module.__source__ if module and getattr(module,'__source__',None) else ''
    if '__str__' in src or '__repr__' in src:
        checks.append('✅ 문제 5: __str__/__repr__ 구현 감지')
    else:
        checks.append('❌ 문제 5: __str__/__repr__ 구현이 보이지 않습니다')

    for c in checks:
        print(c)

    # comment heuristic
    try:
        if module is not None and getattr(module, '__source__', None):
            lines = module.__source__.splitlines()
        else:
            with open('week10_class.py','r',encoding='utf-8') as f:
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
