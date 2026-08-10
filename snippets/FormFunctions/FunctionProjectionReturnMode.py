def script_outputs(*args):
    projection_value = get_projection_value(*args)

    if not is_return_mode_forker(*args) and is_operation_mode_multiple(*args):
        if projection_value == 'without_data':
            return '__ENTITY__S_WITHOUT_DATA'

        if projection_value == 'id_only':
            return '__ENTITY__S_ID_ONLY'

        return '__ENTITY__S'

    if projection_value == 'without_data':
        return '__ENTITY___WITHOUT_DATA'

    if projection_value == 'id_only':
        return '__ENTITY___ID_ONLY'

    return '__ENTITY__'
