from everysk.core.datetime import Date

datastore_output: BaseDict = None
storage_settings: BaseDict = None

output_datastore: Datastore = None

def _initialize_output_datastore(self) -> None:
    """
    Initializes a `Datastore` object with form data and default fallback values.
    """
    self.output_datastore = Datastore(**self.datastore_output)
    self.output_datastore.workspace = self.output_datastore.workspace or self.workspace
    self.output_datastore.date = self.output_datastore.date or Date.today()

def _finalize_output_datastore(self) -> None:
    """
    Finalizes a `Datastore` object filling data and stores it accordingly.
    """
    self.output_datastore.data = __DATA__
    self.output_datastore = Datastore.script.storage(self.output_datastore, self.storage_settings)
