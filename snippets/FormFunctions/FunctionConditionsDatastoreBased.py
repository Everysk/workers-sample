
def get_condition_operator_value(*args):
    assembler_line = args[2]
    operator = assembler_line.get('operator', {})
    select = operator.get('select', {})
    return select.get('value', '')

def is_nullary_condition_operator(*args):
    return get_condition_operator_value(*args) not in {'exists', 'not_exists', 'is_empty', 'not_is_empty'}
