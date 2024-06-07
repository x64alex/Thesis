import unittest
from unittest.mock import patch
import tempfile
import json
from JCML.interpret import JCML, JCMLMatchingStrategy

class TestJCML(unittest.TestCase):

    def setUp(self):
        self.mock_configuration = {
            "matches": [{"pattern": "HELLO", "responses": ["Hi there!", "Hello!"]}],
            "types": {"greeting": ["HELLO", "HI"], "farewell": ["BYE", "GOODBYE"]},
            "functions": {"function_name":"./"}
        }
        self.temp_config_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        json.dump(self.mock_configuration, self.temp_config_file)
        self.temp_config_file.close()
        self.jcml = JCML(filename=self.temp_config_file.name, matching_strategy=JCMLMatchingStrategy())

    def tearDown(self):
        import os
        os.unlink(self.temp_config_file.name)

    def test_get_response_empty_input(self):
        response = self.jcml.get_response('')
        self.assertEqual(response, self.jcml.bad_response)

    def test_get_response_invalid_input(self):
        response = self.jcml.get_response('Some random input')
        self.assertEqual(response, self.jcml.bad_response)

    def test_get_response_valid_input(self):
        response = self.jcml.get_response('HELLO')
        self.assertIn(response, ["Hi there!", "Hello!"])

    def test_get_response_valid_input_with_variable(self):
        pattern = "@@greeting"
        responses = ["Hi!", "Hello!"]
        self.jcml.categories = [{"pattern": pattern, "responses": responses}]
        response = self.jcml.get_response('HELLO')
        self.assertIn(response, responses)

    @patch('JCML.interpret.os.path.exists')
    def test_callFunction_file_not_exists(self, mock_exists):
        mock_exists.return_value = False
        function_method = "@$function_name(param1,param2)"
        result = self.jcml.callFunction(function_method)
        self.assertEqual(result, self.jcml.bad_response)

    def test_match_pattern_exact_match(self):
        strategy = JCMLMatchingStrategy()
        input_text = "HELLO"
        pattern = "HELLO"
        types = {}
        variables = {}
        self.assertTrue(strategy.match_pattern(input_text, pattern, types, variables))

    def test_match_pattern_with_type(self):
        strategy = JCMLMatchingStrategy()
        input_text = "HELLO"
        pattern = "@@GREETING"
        types = {"greeting": ["HELLO", "HI"]}
        variables = {}
        self.assertTrue(strategy.match_pattern(input_text, pattern, types, variables))
        self.assertEqual(variables, {"@@GREETING": "HELLO"})

    def test_match_pattern_with_star(self):
        strategy = JCMLMatchingStrategy()
        input_text = "ANYTHING"
        pattern = "*"
        types = {}
        variables = {}
        self.assertTrue(strategy.match_pattern(input_text, pattern, types, variables))

    def test_getParametersValues(self):
        parameters = ["@@param1", "param2"]
        self.jcml.variables = {"@@param1": "value1"}
        updated_parameters = self.jcml.getParametersValues(parameters)
        self.assertEqual(updated_parameters, ["value1", "param2"])

if __name__ == '__main__':
    unittest.main()
