import json
import random
import re
import os
import importlib.util
from abc import ABC, abstractmethod

class MatchingStrategy(ABC):
    @abstractmethod
    def match_pattern(self, input_text, pattern, types, variables):
        pass


class JCMLMatchingStrategy(MatchingStrategy):
    def match_pattern(self, input_text, pattern, types, variables):
        input_words = input_text.upper().split()
        pattern_words = pattern.upper().split()

        if len(input_words) != len(pattern_words):
            return False

        for input_word, pattern_word in zip(input_words, pattern_words):
            if pattern_word.startswith("@@"):
                filtered_word = ''.join(filter(str.isalpha, pattern_word[2:])).lower()
                if filtered_word not in types:
                    return False
                words = types[filtered_word]
                if input_word not in words:
                    return False
                variables[pattern_word] = input_word
            elif pattern_word != '*' and input_word != pattern_word:
                return False
        return True

class JCML:
    def __init__(self, filename, matching_strategy = JCMLMatchingStrategy()):
        self.categories, self.types, self.functions = self.load_configuration(filename)
        self.variables = {}
        self.bad_response = "Sorry, I didn't understand that."
        self.filename = filename
        self.matching_strategy = matching_strategy

    def get_response(self, input_text):
        input_text = input_text.strip()
        for category in self.categories:
            pattern = category.get('pattern', '').strip()
            responses = category.get('responses', [])

            if self.matching_strategy.match_pattern(input_text, pattern, self.types, self.variables):
                response = random.choice(responses)
                return self.complete_response(response)

        return self.bad_response

    def update_configuration(self, new_data):
        print(new_data)
        with open(self.filename, 'w') as file:
            json.dump(new_data, file)


    def load_configuration(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)

        categories = data.get('matches', [])
        types = data.get('types', [])
        functions = data.get('functions', [])
        return categories, types, functions

    def getParametersValues(self, parameters):
        updated_parameters = []
        for parameter in parameters:
            if parameter.startswith("@@"):
                updated_parameters.append(self.variables.get(parameter, parameter))
            else:
                updated_parameters.append(parameter)
        return updated_parameters

    def callFunction(self, functionMethod):
        pattern = r'@\$(\w+)\((.*)\)'
        match = re.match(pattern, functionMethod)
        if match:
            function_name = match.group(1)
            parameters = self.getParametersValues(match.group(2).split(','))
            
            if function_name in self.functions.keys():
                file_path = os.path.join(self.functions[function_name], f"{function_name}.py")
                if os.path.exists(file_path):
                    spec = importlib.util.spec_from_file_location(function_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                else:
                    print(f"File '{file_path}' not found.")
                    return self.bad_response
            else:
                module_name = f"functions.{function_name}"
                if function_name in self.functions.keys():
                    module_name = self.functions[function_name]+'.'+function_name
                spec = importlib.util.find_spec(module_name)
            
            if spec is not None:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, function_name):
                    function = getattr(module, function_name)
                    result = function(*parameters)
                    return result
                else:
                    print(f"Function '{function_name}' not found in module '{module_name}'.")
            else:
                print(f"Module '{module_name}' not found.")
            return self.bad_response


    def complete_response(self, response):
        pattern = r'@\$\w+\([^)]*\)|@@\w+'

        def replace(match):
            word = match.group(0)
            if word[:2] == "@$":
                return self.callFunction(word)
            return self.variables.get(word, word)

        matched_words = re.findall(pattern, response)
        unmatched_words = [word for word in matched_words if word[:2] == "@@" and word not in self.variables]

        if unmatched_words:
            return self.bad_response

        replaced_response = re.sub(pattern, replace, response)
        return replaced_response

if __name__ == "__main__":
    jcml = JCML('chatConfiguration.json')
    
    while True:
        user_input = input("You: ")
        response = jcml.get_response(user_input)
        print("Bot:", response)
