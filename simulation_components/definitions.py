import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

TEST_DIR = os.path.join(ROOT_DIR, 'tests')
TEST_RES_DIR = os.path.join(TEST_DIR, 'resources')

OBSERVABILITY = True

LOGGING_PATH = os.path.join(ROOT_DIR, 'logs', 'trace_log01.csv')
LOGGING_PATH_TEST = os.path.join(TEST_RES_DIR, 'logs', 'trace_log01.csv')
