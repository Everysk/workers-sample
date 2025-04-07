###############################################################################
##
##  (C) Copyright 2023 EVERYSK TECHNOLOGIES
##
##  This is an unpublished work containing confidential and proprietary
##  information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
##  without authorization of EVERYSK TECHNOLOGIES is prohibited.
##
###############################################################################

###############################################################################
# Imports
###############################################################################

from everysk.core.object import BaseDict
from everysk.sdk.worker_base import WorkerBase

from utils import sample_function

###############################################################################
# Implementation
###############################################################################

class WorkerSample(WorkerBase):
    """
    A class representing a Sample worker that handles inputs, outputs, and tasks.

    Attributes:
        workflow_outputs (dict): A dictionary to store workflow outputs.
    """
    args: dict = None

    def _process_data(self):
        """
        Internal function to process de data and generate new data.
        """
        self.args['new_value'] = sample_function('test')

    def handle_inputs(self) -> None:
        """
        Handles the input data for the worker .
        """
        self.args = self.script_inputs

    def handle_outputs(self) -> dict:
        """
        Handles the output data for the worker.

        Returns:
            dict: The worker outputs.
        """
        return self.args

    def handle_tasks(self) -> None:
        """
        Handles the tasks for the worker.
        """
        self._process_data()

def main(args: BaseDict) -> dict:
    """
    The main function that runs the Sample worker.

    Args:
        args (BaseDict): The input arguments for the worker.

    Returns:
        dict: The result of running the worker.
    """
    return WorkerSample(args).run()
