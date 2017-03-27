#! /usr/bin/python

"""Implement a command line utility which support several optional mutually
exclusive parameters and  should provide next functionality:
-          < --human > - Execute and parse linux system command "df -h";
-          < --inode > Execute and parse linux system command "df -i";
-          In case of no options execute "df";

Output JSON dict to stdout with the following keys:
"status": "success" | "failure"
"error": "<error message>" | "None"
"result": "None" or dictionary with the following keys:
    In case of "df -h": [Filesystem, Size, Used, Avail, Use%, Mounted on]
    In case of "df -i": [Filesystem, Inodes, IUsed, IFree, IUse%, Mounted on]
    In case of "df": [Filesystem, 1K-blocks, Used, Available, Use%, Mounted on]

Utility should use python 2.7.x, json, subprocess.Popen, argrapse ;
Utility should be written according to OOP principles:
-Separate class for executors with base class;
-Separate class for parsers with base class;
-Executor classes should encapsulate parser classes;"""

import argparse
import subprocess
import json
import re


class BaseBuilder(object):
    """class to make a command and run it shell"""
    def __init__(self, cmd='df', *args):
        self.cmd = cmd
        self.args = args
        self.parser_cls = BaseParser

    def build_a_command(self):
        """makes a command from arguments"""
        command = list()
        command.append(self.cmd)
        if self.args:
            for arg in self.args:
                command.append(arg)
        return command

    def execute(self):
        """execute command in shell -> output, error and return code"""
        command = self.build_a_command()
        data = subprocess.Popen(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        output_data, error = data.communicate()
        return_code = data.returncode
        if return_code == 0:
            out = self.parser_cls(output_data).make_string_as_dict()
            return Result(out, str(error), return_code)
        else:
            return Result(None, str(error), return_code)


class BuilderHuman(BaseBuilder):
    """class to execute command in shell with default arguments"""
    def __init__(self):
        super(BuilderHuman, self).__init__('df', '-h')
        self.parser_cls = HumanParser


class BuilderInode(BaseBuilder):
    """class to execute command in shell with default arguments"""
    def __init__(self):
        super(BuilderInode, self).__init__('df', '-i')
        self.parser_cls = InodeParser


class Result(object):
    """class to compile the final output and return it as json"""
    def __init__(self, stdout, stderr, exit_code):
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code

    def to_json(self):
        """Serialize output to a json format"""
        if self.exit_code:
            status = 'Failure'
        else:
            status = 'Success'
        as_dict = {
            'status': status,
            'error': self.stderr,
            'result': self.stdout
        }
        json_data = json.dumps(as_dict, sort_keys=True,
                               indent=4, separators=(',', ': '))
        return json_data


class BaseParser(object):
    """class to make object as dict from shell output"""
    def __init__(self, string):
        self.string = string
        self. output_dict = {}
        self.array_names = ['Filesystem', '1K-blocks', 'Used',
                            'Available', 'Use%', 'Mounted on']
        self.template = (r'(?P<first>\S+)\s*(?P<second>\d+)\s*'
                         r'(?P<third>\d+)\s*(?P<fourth>\d+)\s*'
                         r'(?P<fifth>\d+[%])\s*(?P<sixth>\S+)')

    def make_string_as_dict(self):
        """find all occurrences of a default pattern in a string and
        compile it to dict"""
        data = re.compile(self.template)
        matched_data = re.findall(data, self.string)
        for single_match in matched_data:
            inserted_dict = {}
            i = 0
            for name in self.array_names:
                inserted_dict[name] = single_match[i]
                i += 1
            filesystem_name = "Filesystem '{}' mounted on '{}'".\
                format(single_match[0], single_match[-1])
            self.output_dict[filesystem_name] = inserted_dict
        return self.output_dict


class HumanParser(BaseParser):
    """class to make object as dict from shell
    output with another pattern"""
    def __init__(self, string):
        super(HumanParser, self).__init__(string)
        self.string = string
        self.array_names = ['Filesystem', 'Size', 'Used',
                            'Avail', 'Use%', 'Mounted on']
        self.template = (r'(?P<first>\S+)\s*(?P<second>\S+)\s*'
                         r'(?P<third>\S+)\s*(?P<fourth>\S+)\s*'
                         r'(?P<fifth>\d+[%])\s*(?P<sixth>\S+)')


class InodeParser(BaseParser):
    """class to make object as dict from shell
    output with another pattern"""
    def __init__(self, string):
        super(InodeParser, self).__init__(string)
        self.string = string
        self.array_names = ['Filesystem', 'Inodes', 'IUsed',
                            'IFree', 'IUse%', 'Mounted on']


if __name__ == '__main__':
    result = None
    error_exit_code = 1
    parser = argparse.ArgumentParser(
        description='Command line utility which supports '
                    'several optional arguments.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--human', action='store_true',
                       help='Device statistics in bytes')
    group.add_argument('--inode', action='store_true',
                       help='Device statistics in inodes')
    try:
        command_args = parser.parse_args()
        if command_args.human:
            result = BuilderHuman().execute()
        elif command_args.inode:
            result = BuilderInode().execute()
        else:
            result = BaseBuilder().execute()
    except Exception as err:
        result = Result(None, str(err), error_exit_code)
    finally:
        if result:
            print result.to_json()
