from everysk.sdk.entities.tags import Tags

datastore_output: BaseDict = None
storage_settings: BaseDict = None

output_datastore: Datastore = None

def _initialize_output_datastore(self) -> None:
    """
    Initializes a `Datastore` object with form data and reference entity fallback values.
    """
    self.output_datastore = Datastore(**self.datastore)

    self.output_datastore.update({
        'name': self.datastore_output.name or self.datastore.name,
        'workspace': self.datastore_output.workspace or self.workspace,
        'date': self.datastore_output.date or self.datastore.date,
        'tags': Tags.unify(self.datastore_output.tags, self.datastore.tags),
        'link_uid': self.datastore_output.link_uid or self.datastore.link_uid,
    })

def _finalize_output_datastore(self) -> None:
    """
    Finalizes a `Datastore` object filling data and stores it accordingly.
    """
    self.output_datastore.data = __DATA__
    self.output_datastore = Datastore.script.storage(self.output_datastore, self.storage_settings)
