from pytest import raises, mark
from src.StringToCodeAdapter import StringToCodeAdapter


adapter = StringToCodeAdapter()

def test_string_to_callable_object():
    one_liner = "sleep(5)"

    python_function = adapter.string_to_function(one_liner)

    assert callable(python_function)

def test_adapted_funcion_returns_variable():
    one_liner = """
x=2
x=x+1
return x
"""

    python_function = adapter.string_to_function(one_liner)

    assert python_function() == 3

def test_adapter_returns_hardcoded_int():
    one_liner = "return 5"

    python_function = adapter.string_to_function(one_liner)

    assert python_function() == 5

def test_adapter_returns_hardcoded_string():
    one_liner = "return 'hello'"

    python_function = adapter.string_to_function(one_liner)

    assert python_function() == 'hello'

def test_adapter_returns_sum():
    one_liner = "return 2+3"

    python_function = adapter.string_to_function(one_liner)

    assert python_function() == 5


def test_adapter_returns_object_property():
    one_liner = """
class TestObject:
    def __init__(self):
        self.y = 'y'

x = TestObject()
return x.y
    """

    python_function = adapter.string_to_function(one_liner)

    assert python_function() == 'y'

def test_adapter_raises():
    one_liner = "return x"

    python_function = adapter.string_to_function(one_liner)

    with raises(NameError):
        python_function()

if __name__ == "__main__":
    test_adapter_returns_object_property()