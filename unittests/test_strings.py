import burger

def test_truefalse():
	assert burger.truefalse(0) == 'false'
	assert burger.truefalse(0.0) == 'false'
	assert burger.truefalse('0') == 'false'
	assert burger.truefalse('FALSE') == 'false'
	assert burger.truefalse('false') == 'false'
	assert burger.truefalse('False') == 'false'
	assert burger.truefalse(False) == 'false'
	assert burger.truefalse([]) == 'false'
	assert burger.truefalse({}) == 'false'
	assert burger.truefalse(()) == 'false'

	assert burger.truefalse(1) == 'true'
	assert burger.truefalse(1.0) == 'true'
	assert burger.truefalse('1') == 'true'
	assert burger.truefalse('TRUE') == 'true'
	assert burger.truefalse('true') == 'true'
	assert burger.truefalse('True') == 'true'
	assert burger.truefalse(True) == 'true'
	assert burger.truefalse([1]) == 'true'
	assert burger.truefalse({1}) == 'true'
	assert burger.truefalse((1)) == 'true'

	assert burger.truefalse('testing') == 'true'

def test_TRUEFALSE():
	assert burger.TRUEFALSE(0) == 'FALSE'
	assert burger.TRUEFALSE(0.0) == 'FALSE'
	assert burger.TRUEFALSE('0') == 'FALSE'
	assert burger.TRUEFALSE('FALSE') == 'FALSE'
	assert burger.TRUEFALSE('false') == 'FALSE'
	assert burger.TRUEFALSE('False') == 'FALSE'
	assert burger.TRUEFALSE(False) == 'FALSE'
	assert burger.TRUEFALSE([]) == 'FALSE'
	assert burger.TRUEFALSE({}) == 'FALSE'
	assert burger.TRUEFALSE(()) == 'FALSE'

	assert burger.TRUEFALSE(1) == 'TRUE'
	assert burger.TRUEFALSE(1.0) == 'TRUE'
	assert burger.TRUEFALSE('1') == 'TRUE'
	assert burger.TRUEFALSE('TRUE') == 'TRUE'
	assert burger.TRUEFALSE('true') == 'TRUE'
	assert burger.TRUEFALSE('True') == 'TRUE'
	assert burger.TRUEFALSE(True) == 'TRUE'
	assert burger.TRUEFALSE([1]) == 'TRUE'
	assert burger.TRUEFALSE({1}) == 'TRUE'
	assert burger.TRUEFALSE((1)) == 'TRUE'

	assert burger.TRUEFALSE('testing') == 'TRUE'


def test_TrueFalse():
	assert burger.TrueFalse(0) == 'False'
	assert burger.TrueFalse(0.0) == 'False'
	assert burger.TrueFalse('0') == 'False'
	assert burger.TrueFalse('FALSE') == 'False'
	assert burger.TrueFalse('false') == 'False'
	assert burger.TrueFalse('False') == 'False'
	assert burger.TrueFalse(False) == 'False'
	assert burger.TrueFalse([]) == 'False'
	assert burger.TrueFalse({}) == 'False'
	assert burger.TrueFalse(()) == 'False'

	assert burger.TrueFalse(1) == 'True'
	assert burger.TrueFalse(1.0) == 'True'
	assert burger.TrueFalse('1') == 'True'
	assert burger.TrueFalse('TRUE') == 'True'
	assert burger.TrueFalse('true') == 'True'
	assert burger.TrueFalse('True') == 'True'
	assert burger.TrueFalse(True) == 'True'
	assert burger.TrueFalse([1]) == 'True'
	assert burger.TrueFalse({1}) == 'True'
	assert burger.TrueFalse((1)) == 'True'

	assert burger.TrueFalse('testing') == 'True'



