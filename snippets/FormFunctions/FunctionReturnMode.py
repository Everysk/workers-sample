def get_operation_mode_value(*args):
    form_data = args[0]
    _WORKER_TAB_NAME_ = form_data.get('_WORKER_TAB_NAME_', {})
    operation_mode = _WORKER_TAB_NAME_.get('operation_mode', {})
    select = operation_mode.get('select', {})
    return select.get('value', '')

def is_operation_mode_multiple(*args):
    return get_operation_mode_value(*args) == 'multiple'

def is_return_mode_forker(*args):
    return get_operation_mode_value(*args) == 'forker'

def get_operation_mode_grid_size(*args):
    return 6 if is_operation_mode_multiple(*args) else 12

def worker_type(*args):
    return 'FORKER' if is_return_mode_forker(*args) and is_operation_mode_multiple(*args) else 'BASIC'
