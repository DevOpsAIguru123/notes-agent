# Python Basics

## Data Types

```python
# Strings
name = "Alice"
greeting = f"Hello, {name}!"  # f-strings (Python 3.6+)

# Lists
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]  # List comprehension

# Dictionaries
user = {"name": "Alice", "age": 30, "active": True}
user.get("email", "N/A")  # Safe access with default

# Sets
unique = {1, 2, 3, 2, 1}  # {1, 2, 3}
```

## Dictionaries

### Creating Dictionaries

```python
# Literal
person = {"name": "Alice", "age": 30}

# From constructor
person = dict(name="Alice", age=30)

# From list of tuples
person = dict([("name", "Alice"), ("age", 30)])

# Dictionary comprehension
squares = {x: x**2 for x in range(6)}  # {0:0, 1:1, 2:4, 3:9, 4:16, 5:25}
```

### Accessing & Modifying

```python
user = {"name": "Alice", "age": 30}

# Access
user["name"]              # "Alice" (raises KeyError if missing)
user.get("email", "N/A")  # "N/A" (safe access with default)

# Add / Update
user["email"] = "alice@example.com"
user.update({"age": 31, "city": "NYC"})  # Update multiple keys

# Remove
del user["city"]                  # Raises KeyError if missing
email = user.pop("email", None)   # Remove and return, default if missing
last = user.popitem()             # Remove and return last inserted pair
```

### Iterating

```python
data = {"a": 1, "b": 2, "c": 3}

# Keys
for key in data:
    print(key)

# Values
for value in data.values():
    print(value)

# Key-value pairs
for key, value in data.items():
    print(f"{key}: {value}")
```

### Merging Dictionaries

```python
defaults = {"color": "blue", "size": 10}
overrides = {"size": 20, "font": "Arial"}

# Unpacking (Python 3.5+)
merged = {**defaults, **overrides}

# Union operator (Python 3.9+)
merged = defaults | overrides

# In-place merge
defaults |= overrides  # Python 3.9+
```

### Useful Methods

| Method | Purpose | Example |
|--------|---------|---------|
| `.keys()` | All keys | `list(d.keys())` |
| `.values()` | All values | `list(d.values())` |
| `.items()` | Key-value pairs | `list(d.items())` |
| `.get(k, default)` | Safe access | `d.get("x", 0)` |
| `.setdefault(k, v)` | Get or set | `d.setdefault("count", 0)` |
| `.pop(k, default)` | Remove & return | `d.pop("x", None)` |
| `.update(other)` | Merge in place | `d.update({"a": 1})` |
| `.copy()` | Shallow copy | `new = d.copy()` |

### Nested Dictionaries

```python
users = {
    "alice": {"age": 30, "role": "admin"},
    "bob": {"age": 25, "role": "user"},
}

# Access nested value
users["alice"]["role"]  # "admin"

# Safe nested access
def deep_get(d, *keys, default=None):
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key, default)
        else:
            return default
    return d

deep_get(users, "alice", "email", default="N/A")  # "N/A"
```

### defaultdict & Counter

```python
from collections import defaultdict, Counter

# defaultdict - auto-creates missing keys
word_groups = defaultdict(list)
for word in ["apple", "bat", "ant", "bear"]:
    word_groups[word[0]].append(word)
# {'a': ['apple', 'ant'], 'b': ['bat', 'bear']}

# Counter - count occurrences
colors = ["red", "blue", "red", "green", "blue", "red"]
counts = Counter(colors)  # Counter({'red': 3, 'blue': 2, 'green': 1})
counts.most_common(2)     # [('red', 3), ('blue', 2)]
```

## Common Patterns

### Unpacking

```python
# Tuple unpacking
x, y, z = (1, 2, 3)

# Star unpacking
first, *rest = [1, 2, 3, 4, 5]  # first=1, rest=[2,3,4,5]

# Dictionary unpacking
defaults = {"color": "blue", "size": 10}
config = {**defaults, "size": 20}  # Override size
```

### Context Managers

```python
# File handling - automatically closes file
with open("data.txt", "r") as f:
    content = f.read()

# Custom context manager
from contextlib import contextmanager

@contextmanager
def timer(label):
    import time
    start = time.time()
    yield
    print(f"{label}: {time.time() - start:.2f}s")

with timer("Processing"):
    do_work()
```

### Error Handling

```python
try:
    result = risky_operation()
except ValueError as e:
    print(f"Bad value: {e}")
except (TypeError, KeyError) as e:
    print(f"Type or key error: {e}")
else:
    print("Success!")  # Runs if no exception
finally:
    cleanup()  # Always runs
```

## Virtual Environments

```bash
# Create and activate
python -m venv .venv
source .venv/bin/activate  # macOS/Linux

# Or use uv (faster)
uv venv
source .venv/bin/activate
uv pip install requests
```

## Useful Built-ins

| Function | Purpose | Example |
|----------|---------|---------|
| `enumerate()` | Index + value | `for i, v in enumerate(lst)` |
| `zip()` | Pair iterables | `for a, b in zip(x, y)` |
| `map()` | Transform items | `map(str.upper, words)` |
| `filter()` | Select items | `filter(None, items)` |
| `any()` / `all()` | Boolean checks | `any(x > 0 for x in nums)` |
| `sorted()` | Sort with key | `sorted(users, key=lambda u: u.age)` |
