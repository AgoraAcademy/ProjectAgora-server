# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class ProjectProjectMeta(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, project_intro: str=None, project_goal: str=None, evaluation_schema: str=None, project_plan: str=None, instruction_plan: str=None):  # noqa: E501
        """ProjectProjectMeta - a model defined in Swagger

        :param project_intro: The project_intro of this ProjectProjectMeta.  # noqa: E501
        :type project_intro: str
        :param project_goal: The project_goal of this ProjectProjectMeta.  # noqa: E501
        :type project_goal: str
        :param evaluation_schema: The evaluation_schema of this ProjectProjectMeta.  # noqa: E501
        :type evaluation_schema: str
        :param project_plan: The project_plan of this ProjectProjectMeta.  # noqa: E501
        :type project_plan: str
        :param instruction_plan: The instruction_plan of this ProjectProjectMeta.  # noqa: E501
        :type instruction_plan: str
        """
        self.swagger_types = {
            'project_intro': str,
            'project_goal': str,
            'evaluation_schema': str,
            'project_plan': str,
            'instruction_plan': str
        }

        self.attribute_map = {
            'project_intro': 'projectIntro',
            'project_goal': 'projectGoal',
            'evaluation_schema': 'evaluationSchema',
            'project_plan': 'projectPlan',
            'instruction_plan': 'instructionPlan'
        }

        self._project_intro = project_intro
        self._project_goal = project_goal
        self._evaluation_schema = evaluation_schema
        self._project_plan = project_plan
        self._instruction_plan = instruction_plan

    @classmethod
    def from_dict(cls, dikt) -> 'ProjectProjectMeta':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Project_projectMeta of this ProjectProjectMeta.  # noqa: E501
        :rtype: ProjectProjectMeta
        """
        return util.deserialize_model(dikt, cls)

    @property
    def project_intro(self) -> str:
        """Gets the project_intro of this ProjectProjectMeta.

        项目简介  # noqa: E501

        :return: The project_intro of this ProjectProjectMeta.
        :rtype: str
        """
        return self._project_intro

    @project_intro.setter
    def project_intro(self, project_intro: str):
        """Sets the project_intro of this ProjectProjectMeta.

        项目简介  # noqa: E501

        :param project_intro: The project_intro of this ProjectProjectMeta.
        :type project_intro: str
        """

        self._project_intro = project_intro

    @property
    def project_goal(self) -> str:
        """Gets the project_goal of this ProjectProjectMeta.

        项目目标  # noqa: E501

        :return: The project_goal of this ProjectProjectMeta.
        :rtype: str
        """
        return self._project_goal

    @project_goal.setter
    def project_goal(self, project_goal: str):
        """Sets the project_goal of this ProjectProjectMeta.

        项目目标  # noqa: E501

        :param project_goal: The project_goal of this ProjectProjectMeta.
        :type project_goal: str
        """

        self._project_goal = project_goal

    @property
    def evaluation_schema(self) -> str:
        """Gets the evaluation_schema of this ProjectProjectMeta.

        项目评价标准  # noqa: E501

        :return: The evaluation_schema of this ProjectProjectMeta.
        :rtype: str
        """
        return self._evaluation_schema

    @evaluation_schema.setter
    def evaluation_schema(self, evaluation_schema: str):
        """Sets the evaluation_schema of this ProjectProjectMeta.

        项目评价标准  # noqa: E501

        :param evaluation_schema: The evaluation_schema of this ProjectProjectMeta.
        :type evaluation_schema: str
        """

        self._evaluation_schema = evaluation_schema

    @property
    def project_plan(self) -> str:
        """Gets the project_plan of this ProjectProjectMeta.

        项目计划  # noqa: E501

        :return: The project_plan of this ProjectProjectMeta.
        :rtype: str
        """
        return self._project_plan

    @project_plan.setter
    def project_plan(self, project_plan: str):
        """Sets the project_plan of this ProjectProjectMeta.

        项目计划  # noqa: E501

        :param project_plan: The project_plan of this ProjectProjectMeta.
        :type project_plan: str
        """

        self._project_plan = project_plan

    @property
    def instruction_plan(self) -> str:
        """Gets the instruction_plan of this ProjectProjectMeta.

        项目指导规划  # noqa: E501

        :return: The instruction_plan of this ProjectProjectMeta.
        :rtype: str
        """
        return self._instruction_plan

    @instruction_plan.setter
    def instruction_plan(self, instruction_plan: str):
        """Sets the instruction_plan of this ProjectProjectMeta.

        项目指导规划  # noqa: E501

        :param instruction_plan: The instruction_plan of this ProjectProjectMeta.
        :type instruction_plan: str
        """

        self._instruction_plan = instruction_plan
