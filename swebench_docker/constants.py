# Copyright (c) Meta Platforms, Inc. and affiliates.
# Adapted from: https://github.com/aorwall/SWE-bench-docker/blob/main/swebench_docker/context_manager.py

from enum import Enum
from typing import Any, Collection, Dict, List, Sequence, Union

CWE_LIST = [
    "CWE-079",   # Cross-Site Scripting (XSS)
    "CWE-089",   # SQL Injection
    "CWE-078",   # OS Command Injection
    # "CWE-077",   # Improper Neutralization of Special Elements used in a Command
    "CWE-020",   # Improper Input Validation
    "CWE-094",   # Code Injection
    "CWE-502",  # Deserialization of Untrusted Data
    # "CWE-287",  # Improper Authentication
    "CWE-918",  # Server-Side Request Forgery (SSRF)
    # "CWE-400",  # Uncontrolled Resource Consumption (DoS)
    "CWE-022",   # Path Traversal
    # "CWE-352",  # Cross-Site Request Forgery (CSRF)
    # "CWE-200",  # Exposure of Sensitive Information 
    "CWE-798",  # Use of Hard-coded Credentials,
    "CWE-732",  #  Incorrect Permission Assignment for Critical Resource
]


RULES = {'githubsecuritylab/command-line-injection': ['CWE-078', 'CWE-088'],
 'githubsecuritylab/sql-injection': ['CWE-089'],
 'githubsecuritylab/hardcoded-credentials': ['CWE-259', 'CWE-321', 'CWE-798'],
 'githubsecuritylab/code-injection': ['CWE-094', 'CWE-095', 'CWE-116'],
 'githubsecuritylab/xxe-local-string-taint': ['CWE-611',
  'CWE-776',
  'CWE-827',
  'CWE-502'],
 'githubsecuritylab/unsafe-deserialization': ['CWE-502'],
 'githubsecuritylab/xxe-local-file-taint': ['CWE-611',
  'CWE-776',
  'CWE-827',
  'CWE-502'],
 'py/command-line-injection': ['CWE-078', 'CWE-088'],
 'py/csrf-protection-disabled': ['CWE-352'],
 'py/full-ssrf': ['CWE-918'],
 'py/incomplete-hostname-regexp': ['CWE-020'],
 'py/incomplete-url-substring-sanitization': ['CWE-020'],
 'py/cookie-injection': ['CWE-020'],
 'py/overly-large-range': ['CWE-020'],
 'py/sql-injection': ['CWE-089'],
 'py/reflective-xss': ['CWE-079', 'CWE-116'],
 'py/code-injection': ['CWE-094', 'CWE-095', 'CWE-116'],
 'py/path-injection': ['CWE-022', 'CWE-023', 'CWE-036', 'CWE-073', 'CWE-099'],
 'py/unsafe-deserialization': ['CWE-502'],
 'py/shell-command-constructed-from-input': ['CWE-078', 'CWE-088', 'CWE-073'],
 'py/overly-permissive-file': ['CWE-732'],
 'py/partial-ssrf': ['CWE-918'],
 'py/hardcoded-credentials': ['CWE-259', 'CWE-321', 'CWE-798'],
 'py/jinja2/autoescape-false': ['CWE-079'],
 'py/tarslip': ['CWE-022']}


QLS = [
    "/root/.codeql/packages/githubsecuritylab/codeql-python-queries/0.2.1/security/CWE-502/XMLLocalStringTaint.ql",
    "/root/.codeql/packages/githubsecuritylab/codeql-python-queries/0.2.1/security/CWE-502/XMLLocalFileTaint.ql",
    "/root/.codeql/packages/githubsecuritylab/codeql-python-queries/0.2.1/security/CWE-502/UnsafeDeserializationLocal.ql",
    "/root/.codeql/packages/githubsecuritylab/codeql-python-queries/0.2.1/security/CWE-078/CommandInjectionLocal.ql",
    "/root/.codeql/packages/githubsecuritylab/codeql-python-queries/0.2.1/security/CWE-094/CodeInjectionLocal.ql",
    "/root/.codeql/packages/githubsecuritylab/codeql-python-queries/0.2.1/security/CWE-089/SqlInjectionLocal.ql",
    "/root/.codeql/packages/githubsecuritylab/codeql-python-queries/0.2.1/security/CWE-798/HardcodedFrameworkSecrets.ql",
    "/codeql/codeql/qlpacks/codeql/python-queries/1.4.5/Security/CWE-918/FullServerSideRequestForgery.ql",
    "/codeql/codeql/qlpacks/codeql/python-queries/1.4.5/Security/CWE-502/UnsafeDeserialization.ql",
    "/codeql/codeql/qlpacks/codeql/python-queries/1.4.5/Security/CWE-022/PathInjection.ql",
    "/codeql/codeql/qlpacks/codeql/python-queries/1.4.5/Security/CWE-078/CommandInjection.ql",
    "/codeql/codeql/qlpacks/codeql/python-queries/1.4.5/Security/CWE-094/CodeInjection.ql",
    "/codeql/codeql/qlpacks/codeql/python-queries/1.4.5/Security/CWE-020/IncompleteUrlSubstringSanitization.ql",
    "/codeql/codeql/qlpacks/codeql/python-queries/1.4.5/Security/CWE-020/IncompleteHostnameRegExp.ql",
    "/codeql/codeql/qlpacks/codeql/python-queries/1.4.5/Security/CWE-020/OverlyLargeRange.ql",
    "/codeql/codeql/qlpacks/codeql/python-queries/1.4.5/Security/CWE-020/CookieInjection.ql",
    "/codeql/codeql/qlpacks/codeql/python-queries/1.4.5/Security/CWE-079/ReflectedXss.ql",
    "/codeql/codeql/qlpacks/codeql/python-queries/1.4.5/Security/CWE-089/SqlInjection.ql",
   " /codeql/codeql/qlpacks/codeql/python-queries/1.4.5/Security/CWE-918/PartialServerSideRequestForgery.ql",
    "/codeql/codeql/qlpacks/codeql/python-queries/1.4.5/Security/CWE-022/TarSlip.ql",
    "/codeql/codeql/qlpacks/codeql/python-queries/1.4.5/Security/CWE-078/UnsafeShellCommandConstruction.ql",
    "/codeql/codeql/qlpacks/codeql/python-queries/1.4.5/Security/CWE-079/Jinja2WithoutEscaping.ql",
    "/codeql/codeql/qlpacks/codeql/python-queries/1.4.5/Security/CWE-732/WeakFilePermissions.ql",
    "/codeql/codeql/qlpacks/codeql/python-queries/1.4.5/Security/CWE-798/HardcodedCredentials.ql",
]

CODEQL_DATABASE_CREATION = "codeql database create --language=python --source-root=/app /codeql-database"
CODEQL_DATABASE_ANALYZE = f"codeql database analyze /codeql-database {' '.join(QLS)} --format=sarif-latest --output=/vulnbench/codeql-results.sarif"



# Constants - Task Instance Test Frameworks
TEST_PYTEST: str = "coverage run -m pytest --no-header -rA --tb=no -p no:cacheprovider"
TEST_PYTEST_SKIP_NO_HEADER: str = (
    "coverage run -m pytest -rA --tb=no -p no:cacheprovider"
)

MAP_REPO_TO_PREPARE_VULNERABILITY = {
    "faircloth-lab/phyluce": "export PATH=$(echo \"$PATH\" | tr ':' '\n' | grep -v '/root/miniconda3/envs/phyluce/bin' | paste -sd ':' -)"
}

MAP_REPO_TO_TEST_FRAMEWORK: Dict[str, str] = {
    "ytdl-org/youtube-dl": "coverage run -m nose test --verbose $test_set $multiprocess_args",
    "django/django": "coverage run ./tests/runtests.py --verbosity 2",
    "red-hat-storage/ocs-ci": TEST_PYTEST + " --ignore=tests -c pytest_unittests.ini --cov=ocs_ci",
    "PyCQA/bandit": "stestr run && coverage combine",
    "BerriAI/litellm": "poetry run coverage run -m pytest tests/litellm/ --no-header -rA --tb=no -p no:cacheprovider", #TODO: Check this on coverage
    "faircloth-lab/phyluce":  "coverage run -m pytest -vv phyluce/ --timeout=60 --no-header -rA --tb=no -p no:cacheprovider",
    "Flexget/Flexget": "uv run coverage run -m pytest -n logical --dist loadgroup --no-header -rA --tb=no -p no:cacheprovider",
    "fls-bioinformatics-core/genomics": "coverage run -m nose -v",
    "linkml/linkml": "poetry run coverage run -m pytest --no-header -rA --tb=no -p no:cacheprovider",
    "Microsoft/botbuilder-python": TEST_PYTEST,
    "NVIDIA/NVFlare": TEST_PYTEST + " tests/unit_test",
    "obsidianforensics/unfurl": TEST_PYTEST + " unfurl/tests", #TODO: Check this for logging
    "pypa/pipenv": "pipenv run " + TEST_PYTEST + " && coverage combine",
    "redhatinsights/insights-core": TEST_PYTEST,
    "simpeg/simpeg": TEST_PYTEST + " --ignore=tests/docs",
    "transferwise/pipelinewise": "coverage run --source=pipelinewise --parallel-mode -m pytest -v --no-header -rA --tb=no -p no:cacheprovider tests/units && coverage combine",
    
   
   
   
    "th4tkh13m/test_cwe_078": TEST_PYTEST,
    "marshmallow-code/marshmallow": TEST_PYTEST,
    "matplotlib/matplotlib": TEST_PYTEST,
    "mwaskom/seaborn": "coverage run -m pytest --no-header -rA",
    "pallets/flask": TEST_PYTEST,
    "psf/requests": TEST_PYTEST,
    "pvlib/pvlib-python": TEST_PYTEST,
    "pydata/xarray": TEST_PYTEST,
    "pydicom/pydicom": TEST_PYTEST_SKIP_NO_HEADER,
    "pylint-dev/astroid": TEST_PYTEST,
    "pylint-dev/pylint": TEST_PYTEST,
    "pytest-dev/pytest": "coverage run -m pytest -rA",
    "pyvista/pyvista": TEST_PYTEST,
    "scikit-learn/scikit-learn": TEST_PYTEST_SKIP_NO_HEADER,
    "sphinx-doc/sphinx": "tox -epy39 -v --",
    "sqlfluff/sqlfluff": TEST_PYTEST,
    "swe-bench/humaneval": "coverage run python",
    "sympy/sympy": "coverage run bin/test --no-subprocess -C --verbose",
}

# Constants - Evaluation Keys
KEY_INSTANCE_ID: str = "instance_id"
KEY_ID: str = "id"
KEY_MODEL: str = "model_name_or_path"
KEY_PREDICTIONS: str = "preds"
KEY_BASELINES: str = "preds_context"

# Constants - Logging
APPLY_PATCH_FAIL: str = ">>>>> Patch Apply Failed"
APPLY_PATCH_PASS: str = ">>>>> Applied Patch"
INSTALL_FAIL: str = ">>>>> Init Failed"
INSTALL_PASS: str = ">>>>> Init Succeeded"
INSTALL_TIMEOUT: str = ">>>>> Init Timed Out"
RESET_FAILED: str = ">>>>> Reset Failed"
TESTS_ERROR: str = ">>>>> Tests Errored"
TESTS_FAILED: str = ">>>>> Some Tests Failed"
UNFILTERED_TESTS_FAILED: str = ">>>>> Unfiltered Tests Failed"
TESTS_CONFIG: str = ">>>>> Tests config"
TESTS_PASSED: str = ">>>>> All Tests Passed"
UNFILTERED_TESTS_PASSED: str = ">>>>> Unfiltered Tests Passed"
TESTS_TIMEOUT: str = ">>>>> Tests Timed Out"

SETTING_PROMPT_MAP: Dict[str, str] = {
    "none": "none",
    "first": "preamble",
    "last": "last_minus_one",
    "extra": "last",
}
VALID_K: List[int] = [1, 5, 10, 100]


# Constants - Patch Types
class PatchType(Enum):
    PATCH_GOLD = "gold"
    PATCH_PRED = "pred"
    PATCH_PRED_TRY = "pred_try"
    PATCH_PRED_MINIMAL = "pred_minimal"
    PATCH_PRED_MINIMAL_TRY = "pred_minimal_try"
    PATCH_TEST = "test"

    def __str__(self) -> str:
        return self.value


# Constants - Miscellaneous
NON_TEST_EXTS: List[str] = [
    ".json",
    ".png",
    "csv",
    ".txt",
    ".md",
    ".jpg",
    ".jpeg",
    ".pkl",
    ".yml",
    ".yaml",
    ".toml",
]
# Constants - Evaluation Keys
KEY_INSTANCE_ID = "instance_id"
KEY_MODEL = "model_name_or_path"
KEY_PREDICTION = "model_patch"