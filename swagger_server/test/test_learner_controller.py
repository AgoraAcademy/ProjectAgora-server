# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.credit_hour_entry import CreditHourEntry  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response201 import InlineResponse201  # noqa: E501
from swagger_server.models.learner import Learner  # noqa: E501
from swagger_server.models.project import Project  # noqa: E501
from swagger_server.test import BaseTestCase


class TestLearnerController(BaseTestCase):
    """LearnerController integration test stubs"""

    def test_learner_get(self):
        """Test case for learner_get

        返回所有的Leaner详细信息
        """
        response = self.client.open(
            '/v1/learner',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_learner_head(self):
        """Test case for learner_head

        返回所有Learner的关键信息
        """
        response = self.client.open(
            '/v1/learner',
            method='HEAD',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_learner_learner_id_credit_hour_get(self):
        """Test case for learner_learner_id_credit_hour_get

        返回一个Learner相关的学时记录
        """
        response = self.client.open(
            '/v1/learner/{learnerId}/creditHour'.format(learnerId=2),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_learner_learner_id_get(self):
        """Test case for learner_learner_id_get

        返回一个Learner的详细信息
        """
        response = self.client.open(
            '/v1/learner/{learnerId}'.format(learnerId=2),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_learner_learner_id_project_get(self):
        """Test case for learner_learner_id_project_get

        返回一个Learner相关的课程
        """
        response = self.client.open(
            '/v1/learner/{learnerId}/project'.format(learnerId=2),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_learner_post(self):
        """Test case for learner_post

        创建一个Learner
        """
        learner = Learner()
        response = self.client.open(
            '/v1/learner',
            method='POST',
            data=json.dumps(learner),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
