def get_storage_settigs_dict(*args):
    form_data = args[0]
    _WORKER_TAB_NAME_ = form_data.get('_WORKER_TAB_NAME_', {})
    return _WORKER_TAB_NAME_.get('storage_settings', {})

def get_storage_mode_value(*args):
    storage_settings = get_storage_settigs_dict(*args)
    storage_mode = storage_settings.get('storage_mode', {})
    select = storage_mode.get('select', {})
    return select.get('value', '')

def get_projection_value(*args):
    storage_settings = get_storage_settigs_dict(*args)
    projection = storage_settings.get('projection', {})
    select = projection.get('select', {})
    return select.get('value', '')

def is_storage_mode_create(*args):
    return get_storage_mode_value(*args) == 'create'

def is_storage_mode_update(*args):
    return get_storage_mode_value(*args) == 'update'

def is_storage_mode_transient(*args):
    return get_storage_mode_value(*args) == 'transient'

def is_storage_mode_create_or_update(*args):
    return get_storage_mode_value(*args) in {'create', 'update'}

def get_storage_mode_grid_size(*args):
    return 6 if is_storage_mode_create_or_update(*args) else 12

def script_outputs(*args):
    projection_value = get_projection_value(*args)

    if projection_value == 'whole' or is_storage_mode_transient(*args):
        return '__ENTITY__'

    if projection_value == 'without_data':
        return '__ENTITY___WITHOUT_DATA'

    if projection_value == 'id_only':
        return '__ENTITY___ID_ONLY'

    return '__ENTITY__'
