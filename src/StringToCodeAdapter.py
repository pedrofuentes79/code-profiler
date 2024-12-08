import re

class StringToCodeAdapter:
    def string_to_function(self, code_string):
        code_string_without_return, expression_to_return = self.parse_return_statement(code_string)

        def wrapper():
            local_context = {}
            exec(code_string_without_return, {}, local_context)
            expression_string = self.evaluate_output(expression_to_return, local_context)
            return eval(expression_string, {}, local_context)
        return wrapper

    def parse_return_statement(self, code_string):
        lines = code_string.splitlines()
        output = None

        # Find and process the return line
        for i, line in enumerate(lines):
            match = re.match(r'\s*return\s+(.*)\s*$', line)  # Matches 'return variable'
            if match:
                output = match.group(1)
                lines.pop(i)  # Remove the return line
                break
        

        # Join the modified code back into a single string
        modified_code = "\n".join(lines)
        return modified_code, output
    
    def evaluate_output(self, expression, local_variables):
        
        if value_from_context := local_variables.get(expression):
            return f"{value_from_context}"
        elif expression.strip().isdigit():
            return f"{expression}"
        else:
            return expression
        



