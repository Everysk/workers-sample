###############################################################################
#
# (C) Copyright 2025 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################

from everysk.core.object import BaseDict
from everysk.sdk.worker_base import WorkerBase


class HelloWorld(WorkerBase):
    phrase: str | None = None
    output = None

    def handle_inputs(self):
        self.phrase = self.script_inputs.phrase

    def handle_tasks(self):
        self.output = self.phrase

    def handle_outputs(self):
        return BaseDict(phrase=self.output)


def main(args: BaseDict) -> BaseDict:
    return HelloWorld(args).run()
