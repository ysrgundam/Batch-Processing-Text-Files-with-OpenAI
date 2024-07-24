def is_valid_table(text):
    lines = text.strip().split('\n')
    if len(lines) < 2:
        return False

    header = lines[0].split('|')
    for line in lines[1:]:
        cells = line.split('|')
        if len(cells) != len(header):
            return False

    return True

def run_tests_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    test_cases = []
    for case in content.strip().split('\n\n'):
        input_text, expected_output = case.split('\n', 1)
        expected_output = expected_output.strip().lower() == 'true'
        test_cases.append({
            "input": input_text,
            "expected_output": expected_output
        })

    for i, test_case in enumerate(test_cases, start=1):
        input_text = test_case["input"]
        expected_output = test_case["expected_output"]
        actual_output = is_valid_table(input_text)

        if actual_output == expected_output:
            result = "PASS"
        else:
            result = "FAIL"

        print(f"Test Case {i}: {result}")
        print(f"  Input:\n{input_text}")
        print(f"  Expected Output: {expected_output}")
        print(f"  Actual Output: {actual_output}")
        print()

# 指定测试用例文件的路径
test_case_file = "test_cases.txt"

# 运行测试用例
run_tests_from_file(test_case_file)