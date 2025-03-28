import ast
import os
import sys
from pathlib import Path


def extract_functions(file_path: str) -> list[str]:
    """Extract all function definitions from a Python file."""
    with open(file_path) as f:
        content = f.read()

    tree = ast.parse(content)
    return [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]


def extract_tested_functions(file_path: str, prefix: str = "test_") -> list[str]:
    """Extract all functions being tested in a test file."""
    if not os.path.exists(file_path):
        return []

    with open(file_path) as f:
        content = f.read()

    tree = ast.parse(content)
    test_funcs = [
        node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name.startswith(prefix)
    ]

    # Extract function names being tested from the test function names
    tested_funcs = set()
    for func in test_funcs:
        if func.startswith(prefix):
            tested_funcs.add(func[len(prefix) :])

    # Also look for direct usage of functions in the test file
    all_functions_used = set()
    for node in ast.walk(tree):
        # Check for function calls
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            all_functions_used.add(node.func.id)
        # Check for imported functions
        elif isinstance(node, ast.ImportFrom) and node.module and "features" in node.module:
            for name in node.names:
                all_functions_used.add(name.name)

    return list(tested_funcs.union(all_functions_used))


def get_feature_test_mapping() -> dict[str, str]:
    """Get mapping from feature files to their corresponding test files."""
    mapping = {}
    base_dir = Path(".")
    src_dir = base_dir / "src" / "recur_scan"

    # Find all feature files in the source directory
    feature_files = list(src_dir.glob("features*.py"))

    # Create mappings
    for feature_file in feature_files:
        # Get path relative to project root
        relative_path = str(feature_file.relative_to(base_dir))
        # Map to test file with matching name
        test_file = f"tests/test_{feature_file.name}"
        mapping[relative_path] = test_file

    return mapping


def check_file_coverage(feature_file: str, test_file: str) -> list[str]:
    """Check test coverage for a specific feature file and its test file."""
    if not os.path.exists(feature_file):
        print(f"Warning: Feature file {feature_file} does not exist.")
        return []

    feature_funcs = extract_functions(feature_file)
    tested_funcs = extract_tested_functions(test_file)

    # Also check the main test_features.py for coverage of any feature file
    if test_file != "tests/test_features.py":
        main_tested_funcs = extract_tested_functions("tests/test_features.py")
        tested_funcs.extend(main_tested_funcs)

    def is_helper(func_name: str) -> bool:
        """Check if a function is likely a helper."""
        # Skip functions that start with underscore
        return func_name.startswith("_")

    # Filter public functions excluding helpers and get_features
    public_feature_funcs = []
    for func in feature_funcs:
        if func == "get_features":  # get_features is used but not directly tested
            continue
        if is_helper(func):
            continue
        public_feature_funcs.append(func)

    # Check for untested functions
    untested = [f for f in public_feature_funcs if f not in tested_funcs]
    return untested


def main() -> None:
    """Check test coverage for all feature files."""
    mapping = get_feature_test_mapping()
    any_failure = False
    all_untested = []

    # Check all mapped files
    for feature_file, test_file in mapping.items():
        if os.path.exists(feature_file):
            untested = check_file_coverage(feature_file, test_file)
            if untested:
                print(f"Error: The following functions in {feature_file} don't have tests in {test_file}:")
                for func in untested:
                    print(f"  - {func}")
                all_untested.extend([f"{Path(feature_file).stem}::{func}" for func in untested])
                any_failure = True

    if any_failure:
        print("\nSummary of untested functions:")
        for func in all_untested:
            print(f"  - {func}")
        sys.exit(1)
    else:
        print("All public functions in feature files have corresponding tests!")
        sys.exit(0)


if __name__ == "__main__":
    main()
