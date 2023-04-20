import pytest
from initial_condition_functions import writing_initial_conditions

name1 = "out.1000000.0000.vtu"
writing_initial_conditions(name1)


if __name__ == "__main__":
    pytest.main(["-q", "--tb=long", "test_.py"])
