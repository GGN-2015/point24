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

if __name__ == "__main__":
    for line in solve(2, 3, 7, 7):
        print(line)
