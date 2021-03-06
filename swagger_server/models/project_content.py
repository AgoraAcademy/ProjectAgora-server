# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class ProjectContent(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, item_title: str=None, item_start_date: str=None, item_end_date: str=None, item_content: str=None, item_record: str=None, item_comment: str=None):  # noqa: E501
        """ProjectContent - a model defined in Swagger

        :param item_title: The item_title of this ProjectContent.  # noqa: E501
        :type item_title: str
        :param item_start_date: The item_start_date of this ProjectContent.  # noqa: E501
        :type item_start_date: str
        :param item_end_date: The item_end_date of this ProjectContent.  # noqa: E501
        :type item_end_date: str
        :param item_content: The item_content of this ProjectContent.  # noqa: E501
        :type item_content: str
        :param item_record: The item_record of this ProjectContent.  # noqa: E501
        :type item_record: str
        :param item_comment: The item_comment of this ProjectContent.  # noqa: E501
        :type item_comment: str
        """
        self.swagger_types = {
            'item_title': str,
            'item_start_date': str,
            'item_end_date': str,
            'item_content': str,
            'item_record': str,
            'item_comment': str
        }

        self.attribute_map = {
            'item_title': 'itemTitle',
            'item_start_date': 'itemStartDate',
            'item_end_date': 'itemEndDate',
            'item_content': 'itemContent',
            'item_record': 'itemRecord',
            'item_comment': 'itemComment'
        }

        self._item_title = item_title
        self._item_start_date = item_start_date
        self._item_end_date = item_end_date
        self._item_content = item_content
        self._item_record = item_record
        self._item_comment = item_comment

    @classmethod
    def from_dict(cls, dikt) -> 'ProjectContent':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Project_content of this ProjectContent.  # noqa: E501
        :rtype: ProjectContent
        """
        return util.deserialize_model(dikt, cls)

    @property
    def item_title(self) -> str:
        """Gets the item_title of this ProjectContent.

        条目标题  # noqa: E501

        :return: The item_title of this ProjectContent.
        :rtype: str
        """
        return self._item_title

    @item_title.setter
    def item_title(self, item_title: str):
        """Sets the item_title of this ProjectContent.

        条目标题  # noqa: E501

        :param item_title: The item_title of this ProjectContent.
        :type item_title: str
        """

        self._item_title = item_title

    @property
    def item_start_date(self) -> str:
        """Gets the item_start_date of this ProjectContent.

        条目开始时间; 若存在关联课程，该条为空  # noqa: E501

        :return: The item_start_date of this ProjectContent.
        :rtype: str
        """
        return self._item_start_date

    @item_start_date.setter
    def item_start_date(self, item_start_date: str):
        """Sets the item_start_date of this ProjectContent.

        条目开始时间; 若存在关联课程，该条为空  # noqa: E501

        :param item_start_date: The item_start_date of this ProjectContent.
        :type item_start_date: str
        """

        self._item_start_date = item_start_date

    @property
    def item_end_date(self) -> str:
        """Gets the item_end_date of this ProjectContent.

        条目结束时间; 若存在关联课程，该条为空  # noqa: E501

        :return: The item_end_date of this ProjectContent.
        :rtype: str
        """
        return self._item_end_date

    @item_end_date.setter
    def item_end_date(self, item_end_date: str):
        """Sets the item_end_date of this ProjectContent.

        条目结束时间; 若存在关联课程，该条为空  # noqa: E501

        :param item_end_date: The item_end_date of this ProjectContent.
        :type item_end_date: str
        """

        self._item_end_date = item_end_date

    @property
    def item_content(self) -> str:
        """Gets the item_content of this ProjectContent.

        条目内容；若存在关联课程，该条为空  # noqa: E501

        :return: The item_content of this ProjectContent.
        :rtype: str
        """
        return self._item_content

    @item_content.setter
    def item_content(self, item_content: str):
        """Sets the item_content of this ProjectContent.

        条目内容；若存在关联课程，该条为空  # noqa: E501

        :param item_content: The item_content of this ProjectContent.
        :type item_content: str
        """

        self._item_content = item_content

    @property
    def item_record(self) -> str:
        """Gets the item_record of this ProjectContent.

        条目记录  # noqa: E501

        :return: The item_record of this ProjectContent.
        :rtype: str
        """
        return self._item_record

    @item_record.setter
    def item_record(self, item_record: str):
        """Sets the item_record of this ProjectContent.

        条目记录  # noqa: E501

        :param item_record: The item_record of this ProjectContent.
        :type item_record: str
        """

        self._item_record = item_record

    @property
    def item_comment(self) -> str:
        """Gets the item_comment of this ProjectContent.

        条目评语  # noqa: E501

        :return: The item_comment of this ProjectContent.
        :rtype: str
        """
        return self._item_comment

    @item_comment.setter
    def item_comment(self, item_comment: str):
        """Sets the item_comment of this ProjectContent.

        条目评语  # noqa: E501

        :param item_comment: The item_comment of this ProjectContent.
        :type item_comment: str
        """

        self._item_comment = item_comment
