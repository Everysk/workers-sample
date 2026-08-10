from everysk.sdk.entities.tags import Tags

custom_index_output: BaseDict = None
storage_settings: BaseDict = None

output_custom_index: CustomIndex = None

def _initialize_output_custom_index(self) -> None:
    """
    Initializes a `Custom Index` object with form data and reference entity fallback values.
    """
    self.output_custom_index = CustomIndex(**self.custom_index)

    self.output_custom_index.update({
        'name': self.custom_index_output.name or self.custom_index.name,
        'currency': self.custom_index_output.currency or self.custom_index.currency,
        'periodicity': self.custom_index_output.periodicity or self.custom_index.periodicity,
        'data_type': self.custom_index_output.data_type or self.custom_index.data_type,
        'base_price': self.custom_index_output.base_price or self.custom_index.base_price,
        'tags': Tags.unify(self.custom_index_output.tags, self.custom_index.tags),
    })

def _finalize_output_custom_index(self) -> None:
    """
    Finalizes a `Custom Index` object filling data and stores it accordingly.
    """
    self.output_custom_index.data = __DATA__
    self.output_custom_index = CustomIndex.script.storage(self.output_custom_index, self.storage_settings)
