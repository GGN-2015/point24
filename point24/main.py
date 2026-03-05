import random

try:
    from .exp_gen import get_all_expressions, solve_exp, fill_exp
except:
    from exp_gen import get_all_expressions, solve_exp, fill_exp

def solve(a:int, b:int, c:int, d:int, ans_aim=24) -> list[str]:
    arr = []
    for line in get_all_expressions():
        ans_now = solve_exp(line, [a, b, c, d])
        if isinstance(ans_now, str):
            continue
        if abs(ans_now - ans_aim) < 1e-8:
            arr.append(line)
    return list(set([
        fill_exp(line, [a, b, c, d])
        for line in arr
    ]))

def rand_question_raw(num_max:int) -> tuple[int, ...]:
    return tuple([random.randint(1, num_max) for _ in range(4)])

def rand_question(num_max:int):
    if num_max < 5 or num_max > 13:
        raise ValueError()
    
    # 直到生成合法的问题为止
    arr = rand_question_raw(num_max)
    while len(solve(*arr)) == 0:
        arr = rand_question_raw(num_max)
    return sorted(arr)

def game(num_max:int):
    question_now = rand_question(num_max)
    print(*question_now)

    input("show ans? (press enter)")

    for line in solve(*question_now):
        print(line)


if __name__ == "__main__":
    game(10)
