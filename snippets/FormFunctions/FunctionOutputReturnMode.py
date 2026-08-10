
def script_outputs(*args):
    if not is_return_mode_forker(*args) and is_operation_mode_multiple(*args):
        return '__RESULT__S'
    return '__RESULT__'
