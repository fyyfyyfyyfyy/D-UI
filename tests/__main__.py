import argparse
import os
import sys
import unittest

current_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(current_path)
sys.path.append(root_path)

# 创建命令行参数解析器
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true", help="显示详细的测试结果")

# 解析命令行参数
args = parser.parse_args()

# 自动发现并加载所有的测试文件
test_loader = unittest.TestLoader()
test_suite = test_loader.discover(current_path, pattern="test_*")

if __name__ == "__main__":
    # 运行测试套件
    verbosity = 2 if args.verbose else 1  # 根据参数决定输出详细级别
    unittest.TextTestRunner(verbosity=verbosity).run(test_suite)
