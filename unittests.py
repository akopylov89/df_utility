#! /usr/bin/python

import unittest
from mock import Mock, patch
from testscript import BaseBuilder, BuilderHuman, Result, \
    BaseParser, HumanParser, InodeParser
import test_data


class TestResult(unittest.TestCase):
    """unittests for class Result"""
    def setUp(self):
        """creation of two test objects - one with data, second with error"""
        self.testobj = Result(test_data.TEST_RESULT_OUTPUT,
                              test_data.ERROR_MESSAGE_OK,
                              test_data.RETURN_CODE_OK)
        self.testobj_error = Result(None, test_data.ERROR_MESSAGE_IF_ERROR,
                                    test_data.RETURN_CODE_ERROR)

    def test_to_json(self):
        """testing of the correct output in json"""
        actual_result = self.testobj.to_json()
        self.assertIsInstance(actual_result, str)
        self.assertIsNotNone(actual_result)
        self.assertIn('/boot', test_data.TEST_RESULT_EXPECTED)
        self.assertNotIn('None', test_data.TEST_RESULT_EXPECTED)
        self.assertEqual(actual_result, test_data.TEST_RESULT_EXPECTED)

    def test_to_json_when_error(self):
        """testing of the correct output in json with error returncode"""
        actual_result = self.testobj_error.to_json()
        self.assertIsInstance(actual_result, str)
        self.assertIsNotNone(actual_result)
        self.assertIn('null', test_data.TEST_RESULT_EXP_ERROR)
        self.assertEqual(actual_result, test_data.TEST_RESULT_EXP_ERROR)


class TestBaseParser(unittest.TestCase):
    """unittests for class BaseParser"""
    def test_make_string_as_dict(self):
        """testing of the correct transformation of string to dict"""
        actual_result = BaseParser(test_data.SUB_DF_OUTPUT).\
            make_string_as_dict()
        self.assertIsNotNone(actual_result)
        self.assertIsInstance(actual_result, dict)
        self.assertDictEqual(actual_result, test_data.EXPECTED_BASEBUILDER_OK)


class TestHumanParser(unittest.TestCase):
    """unittests for class HumanParser"""
    def test_make_string_as_dict(self):
        """testing of the correct transformation of string to dict"""
        actual_result = HumanParser(test_data.SUB_DF_H_OUTPUT)\
            .make_string_as_dict()
        self.assertIsNotNone(actual_result)
        self.assertIsInstance(actual_result, dict)
        self.assertDictEqual(actual_result, test_data.EXPECTED_HUMAN_OK)


class TestInodeParser(unittest.TestCase):
    """unittests for class HumanParser"""
    def test_make_string_as_dict(self):
        """testing of the correct transformation of string to dict"""
        actual_result = InodeParser(test_data.SUB_DF_I_OUTPUT)\
            .make_string_as_dict()
        self.assertIsNotNone(actual_result)
        self.assertIsInstance(actual_result, dict)
        self.assertDictEqual(actual_result, test_data.EXPECTED_INODEPARSER)


class TestBaseBuilder(unittest.TestCase):
    """unittests for class BaseBuilder"""
    def test_build_command(self):
        """testing of the correct convertation list of args from *args"""
        self.assertEqual(BaseBuilder().cmd, 'df')
        self.assertEqual(BaseBuilder('ls', 'arg1', 'arg2').args,
                         ('arg1', 'arg2'))
        self.assertIsInstance(BaseBuilder('df', '-i').build_a_command(), list)
        self.assertEqual(BaseBuilder('df', 'h', 'r', 'q').build_a_command(),
                         ['df', 'h', 'r', 'q'],
                         'Error in build_a_command() method')

    def test_execute(self):
        """testing of the correct output of 'df' command when returncode is 0,
        output - str, error_mes, returncode"""
        with patch('script.subprocess.Popen') as mock_subproc_popen:
            communicate_mock = Mock()
            attrs = {'communicate.return_value': (test_data.SUB_DF_OUTPUT,
                                                  test_data.ERROR_MESSAGE_OK),
                     'returncode': test_data.RETURN_CODE_OK}
            communicate_mock.configure_mock(**attrs)
            mock_subproc_popen.return_value = communicate_mock
            actual_result = BaseBuilder().execute()
            self.assertIsNotNone(actual_result.stdout)
            self.assertEqual(actual_result.exit_code, test_data.RETURN_CODE_OK)
            self.assertEqual(actual_result.stderr, test_data.ERROR_MESSAGE_OK)
            self.assertDictEqual(actual_result.stdout,
                                 test_data.EXPECTED_BASEBUILDER_OK)
            self.assertTrue(mock_subproc_popen.called)

    def test_execute_with_error(self):
        """testing of the correct output of 'df' command when returncode is 1,
        output - str, error_mes, returncode"""
        with patch('script.subprocess.Popen') as mock_subproc_popen:
            communicate_mock = Mock()
            attrs = {'communicate.return_value':
                         (test_data.SUB_DF_OUTPUT,
                          test_data.ERROR_MESSAGE_IF_ERROR),
                     'returncode': test_data.RETURN_CODE_ERROR}
            communicate_mock.configure_mock(**attrs)
            mock_subproc_popen.return_value = communicate_mock
            actual_result = BaseBuilder().execute()
            self.assertIsNone(actual_result.stdout)
            self.assertEqual(actual_result.exit_code,
                             test_data.RETURN_CODE_ERROR)
            self.assertEqual(actual_result.stderr,
                             test_data.ERROR_MESSAGE_IF_ERROR)
            self.assertTrue(mock_subproc_popen.called)


class TestBuilderHuman(unittest.TestCase):
    """unittests for class BuilderHuman"""
    def test_build_command(self):
        """testing of the correct convertation to list of args from *args"""
        self.assertEqual(BuilderHuman().cmd, 'df',
                         'Error in HumanBuilder cmd')
        self.assertEqual(BuilderHuman().args, ('-h',),
                         'Error in HumanBuilder arg')
        self.assertEqual(BuilderHuman().build_a_command(), ['df', '-h'],
                         'Error in build_a_command() method')

    def test_execute(self):
        """testing of the correct output of 'df -h' command when returncode
        is 0, output - str, error_mes, returncode"""
        with patch('script.subprocess.Popen') as mock_subproc_popen:
            communicate_mock = Mock()
            attrs = {'communicate.return_value': (test_data.SUB_DF_H_OUTPUT,
                                                  test_data.ERROR_MESSAGE_OK),
                     'returncode': test_data.RETURN_CODE_OK}
            communicate_mock.configure_mock(**attrs)
            mock_subproc_popen.return_value = communicate_mock
            actual_result = BuilderHuman().execute()
            self.assertIsNotNone(actual_result.stdout)
            self.assertEqual(actual_result.exit_code, test_data.RETURN_CODE_OK)
            self.assertEqual(actual_result.stderr, test_data.ERROR_MESSAGE_OK)
            self.assertDictEqual(actual_result.stdout,
                                 test_data.EXPECTED_HUMAN_OK)
            self.assertTrue(mock_subproc_popen.called)

    def test_execute_with_error(self):
        """testing of the correct output of 'df -h' command when returncode
        is 1, output - str, error_mes, returncode"""
        with patch('script.subprocess.Popen') as mock_subproc_popen:
            communicate_mock = Mock()
            attrs = {'communicate.return_value':
                         (test_data.SUB_DF_OUTPUT,
                          test_data.ERROR_MESSAGE_IF_ERROR),
                     'returncode': test_data.RETURN_CODE_ERROR}
            communicate_mock.configure_mock(**attrs)
            mock_subproc_popen.return_value = communicate_mock
            actual_result = BuilderHuman().execute()
            self.assertIsNone(actual_result.stdout)
            self.assertEqual(actual_result.exit_code, test_data
                             .RETURN_CODE_ERROR)
            self.assertEqual(actual_result.stderr,
                             test_data.ERROR_MESSAGE_IF_ERROR)
            self.assertTrue(mock_subproc_popen.called)


if __name__ == '__main__':
    unittest.main(exit=False)
