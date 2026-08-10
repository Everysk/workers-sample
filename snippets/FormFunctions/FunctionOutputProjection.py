def script_outputs(*args):
    projection_value = get_projection_value(*args)

    if projection_value == 'whole' or is_storage_mode_transient(*args):
        return '__ENTITY__'

    if projection_value == 'without_data':
        return '__ENTITY___WITHOUT_DATA'

    if projection_value == 'id_only':
        return '__ENTITY___ID_ONLY'

    return '__ENTITY__'
