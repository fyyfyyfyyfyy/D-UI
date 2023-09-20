# D-UI
an application as User Interface of D-model

## Preparation

1. Install Python Requirements

```bash
pip install -r requirements.txt
```

2. Install pre-commit

```bash
pre-commit install
```

3. Execute `main.py`

```bash
python main.py
```

4. Unittests

```bash
# install unittest dependencies
python -m pip install pytest pytest-cov

# test all test_cases
python -m pytest tests/

# test specified test_case
python -m tests/test_decimalList.py
```
