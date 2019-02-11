# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.project import Project  # noqa: E501
from swagger_server.test import BaseTestCase


class TestProjectsController(BaseTestCase):
    """ProjectsController integration test stubs"""

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


if __name__ == '__main__':
    import unittest
    unittest.main()
