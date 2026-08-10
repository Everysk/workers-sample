def get_date_mode_value(*args):
    form_data = args[0]
    _WORKER_TAB_NAME_ = form_data.get('_WORKER_TAB_NAME_', {})
    date_mode = _WORKER_TAB_NAME_.get('date_mode', {})
    date_mode_select = date_mode.get('select', {})
    return date_mode_select.get('value', '')

def is_single_date(*args):
    return get_date_mode_value(*args) == 'single_date'

def is_date_interval(*args):
    return get_date_mode_value(*args) == 'date_interval'
