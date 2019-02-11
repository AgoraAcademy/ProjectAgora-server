# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.learner_medical_info_food_alergy import LearnerMedicalInfoFoodAlergy  # noqa: F401,E501
from swagger_server.models.learner_medical_info_medication_allergy import LearnerMedicalInfoMedicationAllergy  # noqa: F401,E501
from swagger_server.models.learner_medical_info_previous_diagnosis import LearnerMedicalInfoPreviousDiagnosis  # noqa: F401,E501
from swagger_server.models.learner_medical_info_regular_medication import LearnerMedicalInfoRegularMedication  # noqa: F401,E501
from swagger_server import util


class LearnerMedicalInfo(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, general_health_status: int=None, blood_type: str=None, last_physical_exam: float=None, previous_diagnosis: List[LearnerMedicalInfoPreviousDiagnosis]=None, regular_medication: List[LearnerMedicalInfoRegularMedication]=None, food_alergy: LearnerMedicalInfoFoodAlergy=None, medication_allergy: LearnerMedicalInfoMedicationAllergy=None):  # noqa: E501
        """LearnerMedicalInfo - a model defined in Swagger

        :param general_health_status: The general_health_status of this LearnerMedicalInfo.  # noqa: E501
        :type general_health_status: int
        :param blood_type: The blood_type of this LearnerMedicalInfo.  # noqa: E501
        :type blood_type: str
        :param last_physical_exam: The last_physical_exam of this LearnerMedicalInfo.  # noqa: E501
        :type last_physical_exam: float
        :param previous_diagnosis: The previous_diagnosis of this LearnerMedicalInfo.  # noqa: E501
        :type previous_diagnosis: List[LearnerMedicalInfoPreviousDiagnosis]
        :param regular_medication: The regular_medication of this LearnerMedicalInfo.  # noqa: E501
        :type regular_medication: List[LearnerMedicalInfoRegularMedication]
        :param food_alergy: The food_alergy of this LearnerMedicalInfo.  # noqa: E501
        :type food_alergy: LearnerMedicalInfoFoodAlergy
        :param medication_allergy: The medication_allergy of this LearnerMedicalInfo.  # noqa: E501
        :type medication_allergy: LearnerMedicalInfoMedicationAllergy
        """
        self.swagger_types = {
            'general_health_status': int,
            'blood_type': str,
            'last_physical_exam': float,
            'previous_diagnosis': List[LearnerMedicalInfoPreviousDiagnosis],
            'regular_medication': List[LearnerMedicalInfoRegularMedication],
            'food_alergy': LearnerMedicalInfoFoodAlergy,
            'medication_allergy': LearnerMedicalInfoMedicationAllergy
        }

        self.attribute_map = {
            'general_health_status': 'generalHealthStatus',
            'blood_type': 'bloodType',
            'last_physical_exam': 'lastPhysicalExam',
            'previous_diagnosis': 'previousDiagnosis',
            'regular_medication': 'regularMedication',
            'food_alergy': 'foodAlergy',
            'medication_allergy': 'medicationAllergy'
        }

        self._general_health_status = general_health_status
        self._blood_type = blood_type
        self._last_physical_exam = last_physical_exam
        self._previous_diagnosis = previous_diagnosis
        self._regular_medication = regular_medication
        self._food_alergy = food_alergy
        self._medication_allergy = medication_allergy

    @classmethod
    def from_dict(cls, dikt) -> 'LearnerMedicalInfo':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Learner_medicalInfo of this LearnerMedicalInfo.  # noqa: E501
        :rtype: LearnerMedicalInfo
        """
        return util.deserialize_model(dikt, cls)

    @property
    def general_health_status(self) -> int:
        """Gets the general_health_status of this LearnerMedicalInfo.

        整体健康状况；0 - 很好（基本不生病，从不住院）； 1 - 一般（偶尔生病住院）； 2 - 欠佳（每个季度都曾生病住院）  # noqa: E501

        :return: The general_health_status of this LearnerMedicalInfo.
        :rtype: int
        """
        return self._general_health_status

    @general_health_status.setter
    def general_health_status(self, general_health_status: int):
        """Sets the general_health_status of this LearnerMedicalInfo.

        整体健康状况；0 - 很好（基本不生病，从不住院）； 1 - 一般（偶尔生病住院）； 2 - 欠佳（每个季度都曾生病住院）  # noqa: E501

        :param general_health_status: The general_health_status of this LearnerMedicalInfo.
        :type general_health_status: int
        """

        self._general_health_status = general_health_status

    @property
    def blood_type(self) -> str:
        """Gets the blood_type of this LearnerMedicalInfo.

        血型  # noqa: E501

        :return: The blood_type of this LearnerMedicalInfo.
        :rtype: str
        """
        return self._blood_type

    @blood_type.setter
    def blood_type(self, blood_type: str):
        """Sets the blood_type of this LearnerMedicalInfo.

        血型  # noqa: E501

        :param blood_type: The blood_type of this LearnerMedicalInfo.
        :type blood_type: str
        """

        self._blood_type = blood_type

    @property
    def last_physical_exam(self) -> float:
        """Gets the last_physical_exam of this LearnerMedicalInfo.

        最近一次体检时间(以年为单位)  # noqa: E501

        :return: The last_physical_exam of this LearnerMedicalInfo.
        :rtype: float
        """
        return self._last_physical_exam

    @last_physical_exam.setter
    def last_physical_exam(self, last_physical_exam: float):
        """Sets the last_physical_exam of this LearnerMedicalInfo.

        最近一次体检时间(以年为单位)  # noqa: E501

        :param last_physical_exam: The last_physical_exam of this LearnerMedicalInfo.
        :type last_physical_exam: float
        """

        self._last_physical_exam = last_physical_exam

    @property
    def previous_diagnosis(self) -> List[LearnerMedicalInfoPreviousDiagnosis]:
        """Gets the previous_diagnosis of this LearnerMedicalInfo.

        既往疾病  # noqa: E501

        :return: The previous_diagnosis of this LearnerMedicalInfo.
        :rtype: List[LearnerMedicalInfoPreviousDiagnosis]
        """
        return self._previous_diagnosis

    @previous_diagnosis.setter
    def previous_diagnosis(self, previous_diagnosis: List[LearnerMedicalInfoPreviousDiagnosis]):
        """Sets the previous_diagnosis of this LearnerMedicalInfo.

        既往疾病  # noqa: E501

        :param previous_diagnosis: The previous_diagnosis of this LearnerMedicalInfo.
        :type previous_diagnosis: List[LearnerMedicalInfoPreviousDiagnosis]
        """

        self._previous_diagnosis = previous_diagnosis

    @property
    def regular_medication(self) -> List[LearnerMedicalInfoRegularMedication]:
        """Gets the regular_medication of this LearnerMedicalInfo.

        长期用药  # noqa: E501

        :return: The regular_medication of this LearnerMedicalInfo.
        :rtype: List[LearnerMedicalInfoRegularMedication]
        """
        return self._regular_medication

    @regular_medication.setter
    def regular_medication(self, regular_medication: List[LearnerMedicalInfoRegularMedication]):
        """Sets the regular_medication of this LearnerMedicalInfo.

        长期用药  # noqa: E501

        :param regular_medication: The regular_medication of this LearnerMedicalInfo.
        :type regular_medication: List[LearnerMedicalInfoRegularMedication]
        """

        self._regular_medication = regular_medication

    @property
    def food_alergy(self) -> LearnerMedicalInfoFoodAlergy:
        """Gets the food_alergy of this LearnerMedicalInfo.


        :return: The food_alergy of this LearnerMedicalInfo.
        :rtype: LearnerMedicalInfoFoodAlergy
        """
        return self._food_alergy

    @food_alergy.setter
    def food_alergy(self, food_alergy: LearnerMedicalInfoFoodAlergy):
        """Sets the food_alergy of this LearnerMedicalInfo.


        :param food_alergy: The food_alergy of this LearnerMedicalInfo.
        :type food_alergy: LearnerMedicalInfoFoodAlergy
        """

        self._food_alergy = food_alergy

    @property
    def medication_allergy(self) -> LearnerMedicalInfoMedicationAllergy:
        """Gets the medication_allergy of this LearnerMedicalInfo.


        :return: The medication_allergy of this LearnerMedicalInfo.
        :rtype: LearnerMedicalInfoMedicationAllergy
        """
        return self._medication_allergy

    @medication_allergy.setter
    def medication_allergy(self, medication_allergy: LearnerMedicalInfoMedicationAllergy):
        """Sets the medication_allergy of this LearnerMedicalInfo.


        :param medication_allergy: The medication_allergy of this LearnerMedicalInfo.
        :type medication_allergy: LearnerMedicalInfoMedicationAllergy
        """

        self._medication_allergy = medication_allergy
