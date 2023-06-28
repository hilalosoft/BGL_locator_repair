import ast
import astpretty
from robot.api.parsing import (
    get_model, Documentation, EmptyLine, KeywordCall,ModelVisitor,
    ModelTransformer, SettingSection, SectionHeader, Token
)
import os
import re

class TestNamePrinter(ModelVisitor):

    def visit_File(self, node):
        print(f"File '{node.source}' has following tests:")
        # Call `generic_visit` to visit also child nodes.
        self.generic_visit(node)

    def visit_TestCaseName(self, node):
        print(f"- {node.name} (on line {node.lineno})")
    
    def visit_Variable(self, node):
        # print(f"- {node.name} (on line {node.lineno}) (value = {node.value[0]})")
        print(node.value[0])
        print(is_valid_css_selector(node.value[0]))
        print(is_valid_xpath_expression(node.value[0]))
        

class TestModifier(ModelTransformer):

    def visit_TestCase(self, node):
        # The matched `TestCase` node is a block with `header` and
        # `body` attributes. `header` is a statement with familiar
        # `get_token` and `get_value` methods for getting certain
        # tokens or their value.
        name = node.header.get_value(Token.TESTCASE_NAME)
        # Returning `None` drops the node altogether i.e. removes
        # this test.
        if name == 'testcase':
            return None
        # Construct new keyword call statement from tokens. See `visit_File`
        # below for an example creating statements using `from_params`.
        new_keyword = KeywordCall([
            Token(Token.SEPARATOR, '    '),
            Token(Token.KEYWORD, 'New Keyword'),
            Token(Token.SEPARATOR, '    '),
            Token(Token.ARGUMENT, 'xxx'),
            Token(Token.EOL)
        ])
        # Add the keyword call to test as the second item.
        node.body.insert(0, new_keyword)
        # No need to call `generic_visit` because we are not
        # modifying child nodes. The node itself must to be
        # returned to avoid dropping it.
        return node

    def visit_File(self, node):
        # Create settings section with documentation. Needed header and body
        # statements are created using `from_params` method. This is typically
        # more convenient than creating statements based on tokens like above.
        settings = SettingSection(
            header=SectionHeader.from_params(Token.SETTING_HEADER),
            body=[
                Documentation.from_params('This is a really\npowerful API!'),
                EmptyLine.from_params()
            ]
        )
        # Add settings to the beginning of the file.
        node.sections.insert(0, settings)
        # Call `generic_visit` to visit also child nodes.
        return self.generic_visit(node)

class ErrorReporter(ModelVisitor):

    # Implement `generic_visit` to visit all nodes.
    def generic_visit(self, node):
        if node.errors:
            print(f'Error on line {node.lineno}:')
            for error in node.errors:
                print(f'- {error}')
        ModelVisitor.generic_visit(self, node)
        
class KeywordRenamer(ModelVisitor):

    def __init__(self, old_name, new_name):
        self.old_name = self.normalize(old_name)
        self.new_name = new_name

    def normalize(self, name):
        return name.lower().replace(' ', '').replace('_', '')

    def visit_KeywordName(self, node):
        '''Rename keyword definitions.'''
        if self.normalize(node.name) == self.old_name:
            token = node.get_token(Token.KEYWORD_NAME)
            token.value = self.new_name

    def visit_KeywordCall(self, node):
        '''Rename keyword usages.'''
        if self.normalize(node.keyword) == self.old_name:
            token = node.get_token(Token.KEYWORD)
            token.value = self.new_name
         
class ErrorReporter(ModelVisitor):

    # Implement `generic_visit` to visit all nodes.
    def generic_visit(self, node):
        if node.errors:
            print(f'Error on line {node.lineno}:')
            for error in node.errors:
                print(f'- {error}')
        ModelVisitor.generic_visit(self, node)

class VariableRenamer(ModelVisitor):

    def __init__(self, old_name, new_name):
        self.old_name = self.normalize(old_name)
        self.new_name = new_name

    def normalize(self, name):
        return name.lower().replace(' ', '').replace('_', '')

    def visit_VariableName(self, node):
        print(node)
        '''Rename keyword definitions.'''
        if self.normalize(node.name) == self.old_name:
            token = node.get_token(Token.VARIABLE_NAME)
            print(token)
            token.value = self.new_name

    def visit_VariableCall(self, node):
        '''Rename keyword usages.'''
        print(node)
        if self.normalize(node.variable) == self.old_name:
            token = node.get_token(Token.VARIABLE)
            token.value = self.new_name

# Check if the string is a valid CSS selector
def is_valid_css_selector(css_selector):
    pattern = re.compile(r'^([a-z0-9_-]+|\*)(#[a-z0-9_-]+)?(\.[a-z0-9_-]+)*(\[[a-z0-9_-]+(=[a-z0-9_-]+)?\])*(:[a-z]+)*$')
    return pattern.match(css_selector) is not None

# Check if the string is a valid XPath expression
def is_valid_xpath_expression(xpath_expression):
    pattern = re.compile(r'^//([a-z0-9_-]+|\*)(\[@[a-z0-9_-]+(=[a-z0-9_-]+)?\])*(/[a-z0-9_-]+(\[@[a-z0-9_-]+(=[a-z0-9_-]+)?\])*)*$')
    return pattern.match(xpath_expression) is not None


def main():
    model = get_model(os.getcwd()+'\\testingRide.robot')
    printer = TestNamePrinter()
    printer.visit(model)
    # robot_files = retreive_robots()
    # for file in robot_files:
    #     robot_model = read_model(file)
    #     dict_variables = retrieve_variables(robot_model)

def retreive_robots():
    pass
def read_model(file):
    pass
def retrieve_variables(robot_model):
    pass
if __name__=="__main__":
    main()
