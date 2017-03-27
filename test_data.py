#! /usr/bin/python

EXPECTED_BASEBUILDER_OK = {"Filesystem 'tmpfs' mounted on '/dev/shm'":
{'Available': '1940904', 'Use%': '1%', 'Used': '156', '1K-blocks': '1941060',
'Filesystem': 'tmpfs', 'Mounted on': '/dev/shm'},
"Filesystem 'tmpfs' mounted on '/sys/fs/cgroup'":
{'Available': '1941060', 'Use%': '0%', 'Used': '0', '1K-blocks': '1941060',
'Filesystem': 'tmpfs', 'Mounted on': '/sys/fs/cgroup'},
"Filesystem '/dev/sr0' mounted on '/run/media/andrei/VBOXADDITIONS_5.1.14_112924'":
{'Available': '0', 'Use%': '100%', 'Used': '57978', '1K-blocks': '57978',
'Filesystem': '/dev/sr0', 'Mounted on': '/run/media/andrei/VBOXADDITIONS_5.1.14_112924'},
"Filesystem '/dev/sda1' mounted on '/boot'":
{'Available': '832672', 'Use%': '20%',
'Used': '205664', '1K-blocks': '1038336', 'Filesystem': '/dev/sda1', 'Mounted on': '/boot'},
"Filesystem 'tmpfs' mounted on '/run/user/1000'":
{'Available': '388204', 'Use%': '1%', 'Used': '12', '1K-blocks': '388216',
'Filesystem': 'tmpfs', 'Mounted on': '/run/user/1000'},
"Filesystem 'tmpfs' mounted on '/run'":
 {'Available': '1932224', 'Use%': '1%', 'Used': '8836', '1K-blocks': '1941060',
 'Filesystem': 'tmpfs', 'Mounted on': '/run'},
 "Filesystem '/dev/mapper/cl-root' mounted on '/'":
 {'Available': '5882604', 'Use%': '43%', 'Used': '4375828', '1K-blocks': '10258432',
 'Filesystem': '/dev/mapper/cl-root', 'Mounted on': '/'},
 "Filesystem 'devtmpfs' mounted on '/dev'":
 {'Available': '1925676', 'Use%': '0%', 'Used': '0', '1K-blocks': '1925676',
 'Filesystem': 'devtmpfs', 'Mounted on': '/dev'}}

SUB_DF_OUTPUT = """
Filesystem          1K-blocks    Used Available Use% Mounted on
/dev/mapper/cl-root  10258432 4375828   5882604  43% /
devtmpfs              1925676       0   1925676   0% /dev
tmpfs                 1941060     156   1940904   1% /dev/shm
tmpfs                 1941060    8836   1932224   1% /run
tmpfs                 1941060       0   1941060   0% /sys/fs/cgroup
/dev/sda1             1038336  205664    832672  20% /boot
tmpfs                  388216      12    388204   1% /run/user/1000
/dev/sr0                57978   57978         0 100% /run/media/andrei/VBOXADDITIONS_5.1.14_112924
"""

EXPECTED_HUMAN_OK = {"Filesystem '/dev/sda1' mounted on '/boot'":
{'Use%': '20%', 'Used': '201M', 'Avail': '814M', 'Filesystem': '/dev/sda1',
'Mounted on': '/boot', 'Size': '1014M'},
"Filesystem '/dev/mapper/cl-root' mounted on '/'": {'Use%': '43%',
'Used': '4.2G', 'Avail': '5.7G', 'Filesystem': '/dev/mapper/cl-root',
'Mounted on': '/', 'Size': '9.8G'},
"Filesystem 'devtmpfs' mounted on '/dev'": {'Use%': '0%', 'Used': '0',
'Avail': '1.9G', 'Filesystem': 'devtmpfs', 'Mounted on': '/dev',
'Size': '1.9G'}}

SUB_DF_H_OUTPUT = """
/dev/mapper/cl-root  9.8G  4.2G  5.7G  43% /
devtmpfs             1.9G     0  1.9G   0% /dev
/dev/sda1           1014M  201M  814M  20% /boot
"""
SUB_DF_I_OUTPUT = """
tmpfs                485265    444  484821    1% /run
tmpfs                485265     16  485249    1% /sys/fs/cgroup
/dev/sda1            524288    337  523951    1% /boot
"""

EXPECTED_INODEPARSER = {"Filesystem 'tmpfs' mounted on '/run'":
                            {'IUse%': '1%', 'IUsed': '444', 'Inodes': '485265',
                             'Filesystem': 'tmpfs', 'Mounted on': '/run',
                             'IFree': '484821'},
                        "Filesystem 'tmpfs' mounted on '/sys/fs/cgroup'":
                            {'IUse%': '1%', 'IUsed': '16', 'Inodes': '485265',
                             'Filesystem': 'tmpfs', 'Mounted on': '/sys/fs/cgroup',
                             'IFree': '485249'},
                        "Filesystem '/dev/sda1' mounted on '/boot'":
                            {'IUse%': '1%', 'IUsed': '337', 'Inodes': '524288',
                             'Filesystem': '/dev/sda1', 'Mounted on': '/boot',
                             'IFree': '523951'}}

TEST_RESULT_OUTPUT = {"Filesystem '/dev/sda1' mounted on '/boot'":
                          {'Available':'832672', 'Use%': '20%',
                           'Used': '205664','1K-blocks': '1038336',
                           'Filesystem': '/dev/sda1','Mounted on': '/boot'}}

TEST_RESULT_EXPECTED = """{
    "error": "",
    "result": {
        "Filesystem '/dev/sda1' mounted on '/boot'": {
            "1K-blocks": "1038336",
            "Available": "832672",
            "Filesystem": "/dev/sda1",
            "Mounted on": "/boot",
            "Use%": "20%",
            "Used": "205664"
        }
    },
    "status": "Success"
}"""

TEST_RESULT_EXP_ERROR = """{
    "error": "Error",
    "result": null,
    "status": "Failure"
}"""

RETURN_CODE_ERROR = 1
RETURN_CODE_OK = 0
ERROR_MESSAGE_OK = ""
ERROR_MESSAGE_IF_ERROR = 'Error'