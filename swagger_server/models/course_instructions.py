# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class CourseInstructions(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, instruction_title: str=None, instruction_start_date: str=None, instruction_end_date: str=None, instruction_content: str=None):  # noqa: E501
        """CourseInstructions - a model defined in Swagger

        :param instruction_title: The instruction_title of this CourseInstructions.  # noqa: E501
        :type instruction_title: str
        :param instruction_start_date: The instruction_start_date of this CourseInstructions.  # noqa: E501
        :type instruction_start_date: str
        :param instruction_end_date: The instruction_end_date of this CourseInstructions.  # noqa: E501
        :type instruction_end_date: str
        :param instruction_content: The instruction_content of this CourseInstructions.  # noqa: E501
        :type instruction_content: str
        """
        self.swagger_types = {
            'instruction_title': str,
            'instruction_start_date': str,
            'instruction_end_date': str,
            'instruction_content': str
        }

        self.attribute_map = {
            'instruction_title': 'instructionTitle',
            'instruction_start_date': 'instructionStartDate',
            'instruction_end_date': 'instructionEndDate',
            'instruction_content': 'instructionContent'
        }

        self._instruction_title = instruction_title
        self._instruction_start_date = instruction_start_date
        self._instruction_end_date = instruction_end_date
        self._instruction_content = instruction_content

    @classmethod
    def from_dict(cls, dikt) -> 'CourseInstructions':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Course_instructions of this CourseInstructions.  # noqa: E501
        :rtype: CourseInstructions
        """
        return util.deserialize_model(dikt, cls)

    @property
    def instruction_title(self) -> str:
        """Gets the instruction_title of this CourseInstructions.

        引导条目标题  # noqa: E501

        :return: The instruction_title of this CourseInstructions.
        :rtype: str
        """
        return self._instruction_title

    @instruction_title.setter
    def instruction_title(self, instruction_title: str):
        """Sets the instruction_title of this CourseInstructions.

        引导条目标题  # noqa: E501

        :param instruction_title: The instruction_title of this CourseInstructions.
        :type instruction_title: str
        """

        self._instruction_title = instruction_title

    @property
    def instruction_start_date(self) -> str:
        """Gets the instruction_start_date of this CourseInstructions.

        引导条目开始时间  # noqa: E501

        :return: The instruction_start_date of this CourseInstructions.
        :rtype: str
        """
        return self._instruction_start_date

    @instruction_start_date.setter
    def instruction_start_date(self, instruction_start_date: str):
        """Sets the instruction_start_date of this CourseInstructions.

        引导条目开始时间  # noqa: E501

        :param instruction_start_date: The instruction_start_date of this CourseInstructions.
        :type instruction_start_date: str
        """

        self._instruction_start_date = instruction_start_date

    @property
    def instruction_end_date(self) -> str:
        """Gets the instruction_end_date of this CourseInstructions.

        引导条目结束时间  # noqa: E501

        :return: The instruction_end_date of this CourseInstructions.
        :rtype: str
        """
        return self._instruction_end_date

    @instruction_end_date.setter
    def instruction_end_date(self, instruction_end_date: str):
        """Sets the instruction_end_date of this CourseInstructions.

        引导条目结束时间  # noqa: E501

        :param instruction_end_date: The instruction_end_date of this CourseInstructions.
        :type instruction_end_date: str
        """

        self._instruction_end_date = instruction_end_date

    @property
    def instruction_content(self) -> str:
        """Gets the instruction_content of this CourseInstructions.

        引导条目内容  # noqa: E501

        :return: The instruction_content of this CourseInstructions.
        :rtype: str
        """
        return self._instruction_content

    @instruction_content.setter
    def instruction_content(self, instruction_content: str):
        """Sets the instruction_content of this CourseInstructions.

        引导条目内容  # noqa: E501

        :param instruction_content: The instruction_content of this CourseInstructions.
        :type instruction_content: str
        """

        self._instruction_content = instruction_content
