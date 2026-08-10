def get_secrets_file_variant(*args):
    form_data = args[0]
    _WORKER_TAB_NAME_ = form_data.get('_WORKER_TAB_NAME_', {})
    _FIELD_ID_ = _WORKER_TAB_NAME_.get('_FIELD_ID_', {})
    return _FIELD_ID_.get('variant', '')


def not_secrets_file_variant_select_secrets(*args):
    return get_secrets_file_variant(*args) != 'selectSecrets'
