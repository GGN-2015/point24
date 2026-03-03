import sympy

import functools
import random
import os
DIRNOW = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(DIRNOW, "data")
TEMP_FILE = os.path.join(DATA_FOLDER, "templates.txt")

# do no need tqdm
try:
    from tqdm import tqdm # type:ignore
except:
    tqdm = lambda x: x

EXP_TEMPLATES = [
    "(((a X b) Y c) Z d)",
    "((a X b) Y (c Z d))",
    "((a X (b Y c)) Z d)",
    "(a X ((b Y c) Z d))",
    "(a X (b Y (c Z d)))"
]

OPE_LIST = [
    "+",
    "-",
    "*",
    "/"
]

def insert_val(term:list, new_val:int) -> list[list[int]]:
    ans = [
        [new_val] + term
    ]
    for i in range(len(term)):
        ans.append(
            term[:i+1] + [new_val] +  term[i+1:]
        )
    return ans

def permutation_all_int(n:int) -> list[list[int]]:
    if n <= 0:
        return [[]] # 一种方案
    last_ans = permutation_all_int(n-1)
    ans = []
    for term in last_ans:
        ans += insert_val(term, n)
    return sorted(ans)

def permutation_all_alpha(n:int=4) -> list[list[str]]:
    last_ans = permutation_all_int(n)
    return [
        [chr((val - 1) + ord("A")) for val in term]
        for term in last_ans
    ]

def fill_exp_template(exp:str, vals:list) -> str:
    assert len(vals) == 4
    for i in range(4):
        exp = exp.replace(chr(ord("a") + i), vals[i])
    return exp

def stringify(val) -> str:
    if isinstance(val, int) or isinstance(val, float):
        if val < 0:
            return f"({val})"
    return str(val)

def fill_exp(exp:str, vals:list) -> str:
    assert len(vals) == 4
    for i in range(4):
        exp = exp.replace(chr(ord("A") + i), stringify(vals[i]))
    return exp

def fill_ope(exp:str, opes:list) -> str:
    assert len(opes) == 3
    for i in range(3):
        exp = exp.replace(chr(ord("X") + i), str(opes[i]))
    return exp

# 计算表达式
def solve_exp(exp:str, vector4:list) -> int|float|str:
    exp = fill_exp(exp, vector4)
    try:
        ans = round(eval(exp), ndigits=6)
    except ZeroDivisionError:
        ans = "err"
    return ans

A, B, C, D = sympy.symbols("A B C D")

@functools.cache
def get_sympy_eval(exp:str):
    return eval(exp)

RANDOM_VECTOR_LIST = [
    [random.random() for _ in range(4)]
    for _ in range(10)
]

@functools.cache
def get_random_vector(exp:str):
    return [
        solve_exp(exp, vector4)
        for vector4 in RANDOM_VECTOR_LIST
    ]

# exp 已经填充了 X, Y, Z 但还没填充 a b c d
def check_same(exp1:str, exp2:str) -> bool:
    if get_random_vector(exp1) != get_random_vector(exp2):
        return False
    exp1_val = get_sympy_eval(exp1)
    exp2_val = get_sympy_eval(exp2)
    diff_expr = sympy.simplify(exp1_val - exp2_val)
    return (diff_expr == 0)

def generate_all_exp() -> list[str]:
    all_exp = []
    for base_exp in EXP_TEMPLATES:
        for num_term in permutation_all_alpha():
            for x_val in OPE_LIST:
                for y_val in OPE_LIST:
                    for z_val in OPE_LIST:
                        exp_now = fill_ope(fill_exp_template(
                            base_exp, num_term), [x_val, y_val, z_val])
                        all_exp.append(exp_now)
    return all_exp

def not_in_arr(arr:list[str], exp:str) -> bool:
    for exp_old in arr:
        if check_same(exp_old, exp):
            return False
    return True

@functools.cache
def generate_all_diff_exp() -> list[str]:
    arr = []
    raw_exp_list = generate_all_exp()
    for i in tqdm(range(len(raw_exp_list))):
        exp = raw_exp_list[i]
        if not_in_arr(arr, exp):
            arr.append(exp)
    return arr

# 创建模板文件
def gen_template_file():
    os.makedirs(DATA_FOLDER, exist_ok=True)

    if os.path.isfile(TEMP_FILE):
        return

    with open(TEMP_FILE, "w") as fp:
        for line in generate_all_diff_exp():
            fp.write(line + "\n")

@functools.cache
def get_all_expressions() -> list[str]:
    gen_template_file()
    return [
        line.strip()
        for line in open(TEMP_FILE)
        if line.strip() != ""
    ]

if __name__ == "__main__":
    gen_template_file()
    print(len(get_all_expressions()))
