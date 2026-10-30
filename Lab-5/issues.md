# Lab 5 – Static Code Analysis: Issue Documentation

**Program:** `delivery_system.py`  
**Analysis tools:** Pylint, Bandit, Flake8  
**Note:** Line numbers below refer to the original, unmodified `delivery_system.py` supplied for the lab.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Missing module docstring | Pylint (C0114) | 1 | The Python module did not have a module-level description. | Added a module docstring describing the program. |
| Non-constant naming for global ID counter | Pylint (C0103) | 7 | `next_id` did not follow the naming convention for a module-level constant. | Replaced the manually incremented counter with `ORDER_IDS = count(1)` and obtained IDs using `next(ORDER_IDS)`. |
| Missing function docstrings | Pylint (C0116) | 11, 21, 27, 35, 42, 47, 51, 56 | Functions did not explain their purpose. | Added a short docstring to each function. |
| Mutable default argument | Pylint (W0102) | 11 | `order_history=[]` is shared between calls when the caller does not provide an argument. | Changed the default to `None` and created a new list inside the function when needed. |
| Use of global statements | Pylint (W0603) | 12, 28, 48 | Functions modified module-level variables using `global`. | Removed the reassignment pattern: used a counter object for IDs and updated the existing `menu` and `orders` dictionaries with `clear()` and `update()`. |
| Bare `except` clause | Pylint (W0702), Flake8 (E722), Bandit (B110) | 24 | A bare exception handler caught every exception and silently ignored it with `pass`, hiding errors. | Removed the broad try/except/pass pattern. `update_order_status()` now checks whether the order ID and status are valid and returns `False` for invalid input. |
| Broad exception handling | Pylint (W0718) | 32 | Catching `Exception` in menu loading could hide unrelated programming errors. | Caught only the expected `FileNotFoundError` and `json.JSONDecodeError` exceptions. |
| File opened without an explicit encoding | Pylint (W1514) | 30 | Text-file reading did not specify an encoding. | Used `encoding="utf-8"` when opening JSON text files. |
| Files not managed with context managers | Pylint (R1732) | 30, 43, 49 | File handles were opened without consistently using a context manager, making reliable closure less clear. | Used `with open(...)` blocks so files are closed automatically. |
| Unsafe pickle deserialization | Bandit (B301) | 49 | `pickle.load()` can execute arbitrary code when loading an untrusted pickle file. | Replaced pickle-based backup and restore with JSON serialization and deserialization. |
| Pickle module imported | Bandit (B403) | 2 | Importing `pickle` was flagged because pickle data is unsafe to deserialize when untrusted. | Removed the `pickle` import after migrating persistence to JSON. |
| Old-style string formatting | Pylint (C0209) | 52 | The queue timestamp used `%` string formatting. | Replaced it with an f-string. |
| Function name did not follow naming convention | Pylint (C0103) | 51 | `printQueue` used mixed-case naming instead of the recommended `snake_case`. | Renamed it to `print_queue`. |
| Missing blank lines between top-level definitions | Flake8 (E302) | 11, 21, 27, 35, 42, 47, 51, 56 | Top-level function definitions did not have the required two blank lines separating them. | Added the required blank lines in accordance with PEP 8. |
| Lines exceeded the recommended maximum length | Flake8 (E501) | 16, 54 | Two source lines exceeded Flake8's 79-character limit. | Wrapped the long expressions and output statement across multiple lines. |

## Verification results

| Tool | Before fixes | After fixes |
|---|---:|---:|
| Pylint | 6.27/10 | 10.00/10 |
| Bandit | 3 findings | 0 findings |
| Flake8 | 11 findings | 0 findings |

The original reports are retained as `pylint_report_before.txt`, `bandit_report_before.txt`, and `flake8_report_before.txt`. The final reports are retained as the corresponding `*_report_after.txt` files.

**Important:** The before/after results above are the results recorded during this lab run. The issue line numbers refer to the original source file, not the cleaned version.
