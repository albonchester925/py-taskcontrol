import pytest


# decorator applied on a function and function invocation creates the task
# decorator creates tasks only on function invocation
# decorator creates instance tasks
# decorator creates shared tasks
class TestDecorator():

    def test_create_task(self):
        pass

    def test_create_instance_task(self):
        pass

    def test_create_shared_task(self):
        pass


# decorator runs instance single tasks
# decorator runs instance multiple tasks
# decorator runs all instance tasks
class TestTaskRunner():

    def test_run_single_instance_task(self):
        pass

    def test_run_multiple_instance_task(self):
        pass

    def test_run_all_instance_task(self):
        pass


# decorator runs shared single task
# decorator runs shared multiple tasks
# decorator runs shared all tasks
class TestSharedTaskRunner():
    def test_run_single_shared_tasks(self):
        pass

    def test_run_single_multiple_tasks(self):
        pass

    def test_run_single_all_shared_tasks(self):
        pass

# decorator runs a mix of instance and shared tasks
class TestAnyTaskRunner():

    def test_any_type_task(self):
        pass

# middlewares can be invoked with arguments and keyword arguments
# middlewares can be invoked and returns (error or next value) after invocation
# middlewares can be invoked and returns (error or next value) after invocation
class TestMiddlewares():

    def test_run_middlewares(self):
        pass

    def test_run_single_middleware(self):
        pass

# functions can be invoked with arguments and keyword arguments
# functions can be invoked and returns (error or next value) after invocation
# functions can be invoked and returns (error or next value) after invocation
class TestFunctions():
    def test_function_invocation_with_arguments(self):
        pass

    def test_function_invocation_returns(self):
        pass

    def test_function_invocation_error_returns(self):
        pass

# middlewares can be invoked and can access results context of all previously invoked functions
class TestMiddlewareAccessContext():
    pass


# functions can be invoked and can access results context of all previously invoked functions
class TestFunctionsAccessContext():
    pass


# middlewares return results
class TestMiddlewaresResultReturns():
    pass


# functions return results
class TestFuctionsResultReturns():
    pass


# task runs return results and correct numbers
class TestTaskResultReturns():
    pass

