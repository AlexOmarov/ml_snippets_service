def setup():
    print("basic setup into module")


def teardown():
    print("basic teardown into module")


def setup_module(module):
    print("module setup")


def teardown_module(module):
    print("module teardown")


def setup_function(function):
    print("function setup")


def teardown_function(function):
    print("function teardown")


def test_numbers_3_4():
    assert 3 * 4 == 12


def test_strings_a_3():
    assert 'a' * 3 == 'aaa'


class TestUM:
    def setup(self):
        print("basic setup into class")

    def teardown(self):
        print("basic teardown into class")

    @classmethod
    def setup_class(cls):
        print("class setup")

    @classmethod
    def teardown_class(cls):
        print("class teardown")

    def setup_method(self, method):
        print("method setup")

    def teardown_method(self, method):
        print("method teardown")

    def test_numbers_5_6(self):
        assert 5 * 6 == 30

    def test_strings_b_2(self):
        assert 'b' * 2 == 'bb'
