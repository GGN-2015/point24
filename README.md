# point24
calculate 24 with four numbers with braces, add, sub, mul and div.

## Install

```bash
pip install point24
```

## Usage

### Solve

```python
import point24

# given four intergers
# output all solutions 
for line in point24.solve(1, 3, 4, 5):
    print(line)
```

### Random Question

```python
import point24

max_num = 13
print(*point24.rand_question(max_num)) # ensured to be feasible
```

### Game

```python
import point24

max_num = 13
point24.game(max_num)
```
