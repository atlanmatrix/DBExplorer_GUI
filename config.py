import os.path


__VERSION__ = '0.4.1'

# # # # # # # #
# Web Config  #
# # # # # # # #
SERVER_NICKNAME = None
# Web server listening port
PORT = 9898
# Request url
BASE_URL = 'http://localhost:9898'

# remember override
MODE = 'DEBUG'
UPLOAD_DIR = 'upload'
LOG_PATH = 'log/debug.log'
# Full path of code dir
FAAS_CODE_DIR = '/tmp'
IN_DOCKER_PATH = '/usr/src/myapp'

# # # # # # # # #
# Authorization #
# # # # # # # # #
DB_DIR = 'db/'


# # # # # # # # #
#      Func     #
# # # # # # # # #
# Max number of function characters
MAX_FUNC_NAME_LENGTH = 32
MAX_FUNC_CODE_LENGTH = 4096


# # # # # # # # # # # # # # # # # # # # #
# interval of service status check(ms)  #
# # # # # # # # # # # # # # # # # # # # #
CHECK_INTERVAL = 5000

# file with following suffix can be directly previewed
TEXT_SUFFIX = {
    '.txt': '',
    '.log': '',
    '.py': 'python',
    '.go': 'go',
    '.c': 'c',
    '.h': 'c',
    '.cpp': 'cpp',
    '.hpp': 'cpp',
    '.sh': 'shell',
    '.sql': 'sql',
    '.xml': 'xml',
    '.htm': 'html',
    '.html': 'html',
    '.xhtml': 'xhtml',
    '.yaml': 'yaml',
    '.css': 'css',
    '.js': 'javascript',
    '.json': 'json',
}

IMG_SUFFIX = [
    '.jpg', '.jpeg', '.png', '.bmp'
]

VIDEO_SUFFIX = [
    '.mp4'
]

MD_SUFFIX = [
    '.md'
]

# remember override
MYSQL_CONF = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'username',
    'password': 'password',
    'database': 'db_name'
}

MONGO_CONF = {
    'host': '127.0.0.1',
    'port': 27017,
    'user': '',
    'password': '',
    'database': 'xiaoya'
}

DIR_NAME = os.path.dirname(__file__)
if os.path.exists(os.path.join(DIR_NAME, 'local_config.py')):
    from local_config import *
