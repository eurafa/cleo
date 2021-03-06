# -*- coding: utf-8 -*-

import os
from io import BytesIO

from ..inputs.list_input import ListInput
from ..outputs.stream_output import StreamOutput


class ApplicationTester(object):
    """
    Eases the testing of console applications.
    """

    def __init__(self, application):
        """
        Constructor

        :param application: A Application instance to test
        :type application: Application
        """
        self.__application = application
        self.__input = None
        self.__output = None
        self.__inputs = []

    def run(self, input_, options=None):
        """
        Executes the command

        Available options:
            * interactive: Sets the input interactive flag
            * decorated: Sets the output decorated flag
            * verbosity: Sets the output verbosity flag

        :param input_: A dict of argument and options
        :type input_: list
        :param options: A dict of options
        :type options: dict

        :return: The command exit code
        :rtype: integer
        """
        options = options or {}

        self.__input = ListInput(input_)
        if self.__inputs:
            self.__input.set_stream(self._create_stream(self.__inputs))

        if 'interactive' in options:
            self.__input.set_interactive(options['interactive'])

        self.__output = StreamOutput(BytesIO())
        if 'decorated' in options:
            self.__output.set_decorated(options['decorated'])
        if 'verbosity' in options:
            self.__output.set_verbosity(options['verbosity'])

        self.__application.run(self.__input, self.__output)

    def get_display(self, normalize=False):
        """
        Gets the display returned by the last execution command

        :return: The display
        :rtype: str
        """
        self.__output.get_stream().seek(0)

        display = self.__output.get_stream().read().decode('utf-8')

        if normalize:
            display = display.replace(os.linesep, '\n')

        return display

    def get_input(self):
        """
        Gets the input instance used by the last execution of the command.

        :return: The current input instance
        :rtype: Input
        """
        return self.__input

    def get_output(self):
        """
        Gets the output instance used by the last execution of the command.

        :return: The current output instance
        :rtype: Output
        """
        return self.__output

    def set_inputs(self, inputs):
        """
        Sets the user inputs.

        :param inputs: The user inputs
        :type inputs: list

        :rtype: CommandTester
        """
        self.__inputs = inputs

        return self

    def _create_stream(self, inputs):
        """
        Create a stream from inputs.

        :type inputs: list

        :rtype:
        """
        stream = BytesIO()
        stream.write(os.linesep.join(inputs).encode())
        stream.seek(0)

        return stream
