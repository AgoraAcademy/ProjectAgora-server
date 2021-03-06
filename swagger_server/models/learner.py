# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.learner_contact_info import LearnerContactInfo  # noqa: F401,E501
from swagger_server.models.learner_custodian_info import LearnerCustodianInfo  # noqa: F401,E501
from swagger_server.models.learner_emergent_contact import LearnerEmergentContact  # noqa: F401,E501
from swagger_server.models.learner_medical_info import LearnerMedicalInfo  # noqa: F401,E501
from swagger_server.models.learner_mentorship import LearnerMentorship  # noqa: F401,E501
from swagger_server import util


class Learner(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, id: int=None, given_name: str=None, family_name: str=None, nickname: str=None, is_mentor: bool=None, gender: str=None, ethnicity: str=None, birthday: str=None, age: float=None, status: str=None, main_personal_id_type: str=None, main_personal_id: str=None, date_of_registration: str=None, reason_of_registration: str=None, previous_status: str=None, date_of_leave: str=None, reason_of_leave: str=None, destination_of_leave: str=None, mentorship: List[LearnerMentorship]=None, salary_card: str=None, custodian_info: List[LearnerCustodianInfo]=None, emergent_contact: List[LearnerEmergentContact]=None, contact_info: LearnerContactInfo=None, medical_info: LearnerMedicalInfo=None, notes: List[str]=None):  # noqa: E501
        """Learner - a model defined in Swagger

        :param id: The id of this Learner.  # noqa: E501
        :type id: int
        :param given_name: The given_name of this Learner.  # noqa: E501
        :type given_name: str
        :param family_name: The family_name of this Learner.  # noqa: E501
        :type family_name: str
        :param nickname: The nickname of this Learner.  # noqa: E501
        :type nickname: str
        :param is_mentor: The is_mentor of this Learner.  # noqa: E501
        :type is_mentor: bool
        :param gender: The gender of this Learner.  # noqa: E501
        :type gender: str
        :param ethnicity: The ethnicity of this Learner.  # noqa: E501
        :type ethnicity: str
        :param birthday: The birthday of this Learner.  # noqa: E501
        :type birthday: str
        :param age: The age of this Learner.  # noqa: E501
        :type age: float
        :param status: The status of this Learner.  # noqa: E501
        :type status: str
        :param main_personal_id_type: The main_personal_id_type of this Learner.  # noqa: E501
        :type main_personal_id_type: str
        :param main_personal_id: The main_personal_id of this Learner.  # noqa: E501
        :type main_personal_id: str
        :param date_of_registration: The date_of_registration of this Learner.  # noqa: E501
        :type date_of_registration: str
        :param reason_of_registration: The reason_of_registration of this Learner.  # noqa: E501
        :type reason_of_registration: str
        :param previous_status: The previous_status of this Learner.  # noqa: E501
        :type previous_status: str
        :param date_of_leave: The date_of_leave of this Learner.  # noqa: E501
        :type date_of_leave: str
        :param reason_of_leave: The reason_of_leave of this Learner.  # noqa: E501
        :type reason_of_leave: str
        :param destination_of_leave: The destination_of_leave of this Learner.  # noqa: E501
        :type destination_of_leave: str
        :param mentorship: The mentorship of this Learner.  # noqa: E501
        :type mentorship: List[LearnerMentorship]
        :param salary_card: The salary_card of this Learner.  # noqa: E501
        :type salary_card: str
        :param custodian_info: The custodian_info of this Learner.  # noqa: E501
        :type custodian_info: List[LearnerCustodianInfo]
        :param emergent_contact: The emergent_contact of this Learner.  # noqa: E501
        :type emergent_contact: List[LearnerEmergentContact]
        :param contact_info: The contact_info of this Learner.  # noqa: E501
        :type contact_info: LearnerContactInfo
        :param medical_info: The medical_info of this Learner.  # noqa: E501
        :type medical_info: LearnerMedicalInfo
        :param notes: The notes of this Learner.  # noqa: E501
        :type notes: List[str]
        """
        self.swagger_types = {
            'id': int,
            'given_name': str,
            'family_name': str,
            'nickname': str,
            'is_mentor': bool,
            'gender': str,
            'ethnicity': str,
            'birthday': str,
            'status': str,
            'main_personal_id_type': str,
            'main_personal_id': str,
            'date_of_registration': str,
            'reason_of_registration': str,
            'previous_status': str,
            'date_of_leave': str,
            'reason_of_leave': str,
            'destination_of_leave': str,
            'mentorship': List[LearnerMentorship],
            'salary_card': str,
            'custodian_info': List[LearnerCustodianInfo],
            'emergent_contact': List[LearnerEmergentContact],
            'contact_info': LearnerContactInfo,
            'medical_info': LearnerMedicalInfo,
            'notes': List[str]
        }

        self.attribute_map = {
            'id': 'id',
            'given_name': 'givenName',
            'family_name': 'familyName',
            'nickname': 'nickname',
            'is_mentor': 'isMentor',
            'gender': 'gender',
            'ethnicity': 'ethnicity',
            'birthday': 'birthday',
            'status': 'status',
            'main_personal_id_type': 'mainPersonalIdType',
            'main_personal_id': 'mainPersonalId',
            'date_of_registration': 'dateOfRegistration',
            'reason_of_registration': 'reasonOfRegistration',
            'previous_status': 'previousStatus',
            'date_of_leave': 'dateOfLeave',
            'reason_of_leave': 'reasonOfLeave',
            'destination_of_leave': 'destinationOfLeave',
            'mentorship': 'mentorship',
            'salary_card': 'salaryCard',
            'custodian_info': 'custodianInfo',
            'emergent_contact': 'emergentContact',
            'contact_info': 'contactInfo',
            'medical_info': 'medicalInfo',
            'notes': 'notes'
        }

        self._id = id
        self._given_name = given_name
        self._family_name = family_name
        self._nickname = nickname
        self._is_mentor = is_mentor
        self._gender = gender
        self._ethnicity = ethnicity
        self._birthday = birthday
        self._status = status
        self._main_personal_id_type = main_personal_id_type
        self._main_personal_id = main_personal_id
        self._date_of_registration = date_of_registration
        self._reason_of_registration = reason_of_registration
        self._previous_status = previous_status
        self._date_of_leave = date_of_leave
        self._reason_of_leave = reason_of_leave
        self._destination_of_leave = destination_of_leave
        self._mentorship = mentorship
        self._salary_card = salary_card
        self._custodian_info = custodian_info
        self._emergent_contact = emergent_contact
        self._contact_info = contact_info
        self._medical_info = medical_info
        self._notes = notes

    @classmethod
    def from_dict(cls, dikt) -> 'Learner':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Learner of this Learner.  # noqa: E501
        :rtype: Learner
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this Learner.

        ID  # noqa: E501

        :return: The id of this Learner.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this Learner.

        ID  # noqa: E501

        :param id: The id of this Learner.
        :type id: int
        """

        self._id = id

    @property
    def given_name(self) -> str:
        """Gets the given_name of this Learner.

        名  # noqa: E501

        :return: The given_name of this Learner.
        :rtype: str
        """
        return self._given_name

    @given_name.setter
    def given_name(self, given_name: str):
        """Sets the given_name of this Learner.

        名  # noqa: E501

        :param given_name: The given_name of this Learner.
        :type given_name: str
        """

        self._given_name = given_name

    @property
    def family_name(self) -> str:
        """Gets the family_name of this Learner.

        姓  # noqa: E501

        :return: The family_name of this Learner.
        :rtype: str
        """
        return self._family_name

    @family_name.setter
    def family_name(self, family_name: str):
        """Sets the family_name of this Learner.

        姓  # noqa: E501

        :param family_name: The family_name of this Learner.
        :type family_name: str
        """

        self._family_name = family_name

    @property
    def nickname(self) -> str:
        """Gets the nickname of this Learner.

        昵称  # noqa: E501

        :return: The nickname of this Learner.
        :rtype: str
        """
        return self._nickname

    @nickname.setter
    def nickname(self, nickname: str):
        """Sets the nickname of this Learner.

        昵称  # noqa: E501

        :param nickname: The nickname of this Learner.
        :type nickname: str
        """

        self._nickname = nickname

    @property
    def is_mentor(self) -> bool:
        """Gets the is_mentor of this Learner.

        是否导师  # noqa: E501

        :return: The is_mentor of this Learner.
        :rtype: bool
        """
        return self._is_mentor

    @is_mentor.setter
    def is_mentor(self, is_mentor: bool):
        """Sets the is_mentor of this Learner.

        是否导师  # noqa: E501

        :param is_mentor: The is_mentor of this Learner.
        :type is_mentor: bool
        """
        if is_mentor is None:
            raise ValueError("Invalid value for `is_mentor`, must not be `None`")  # noqa: E501

        self._is_mentor = is_mentor

    @property
    def gender(self) -> str:
        """Gets the gender of this Learner.

        性别  # noqa: E501

        :return: The gender of this Learner.
        :rtype: str
        """
        return self._gender

    @gender.setter
    def gender(self, gender: str):
        """Sets the gender of this Learner.

        性别  # noqa: E501

        :param gender: The gender of this Learner.
        :type gender: str
        """

        self._gender = gender

    @property
    def ethnicity(self) -> str:
        """Gets the ethnicity of this Learner.

        民族  # noqa: E501

        :return: The ethnicity of this Learner.
        :rtype: str
        """
        return self._ethnicity

    @ethnicity.setter
    def ethnicity(self, ethnicity: str):
        """Sets the ethnicity of this Learner.

        民族  # noqa: E501

        :param ethnicity: The ethnicity of this Learner.
        :type ethnicity: str
        """

        self._ethnicity = ethnicity

    @property
    def birthday(self) -> str:
        """Gets the birthday of this Learner.

        生日  # noqa: E501

        :return: The birthday of this Learner.
        :rtype: str
        """
        return self._birthday

    @birthday.setter
    def birthday(self, birthday: str):
        """Sets the birthday of this Learner.

        生日  # noqa: E501

        :param birthday: The birthday of this Learner.
        :type birthday: str
        """

        self._birthday = birthday

    @property
    def age(self) -> float:
        """Gets the age of this Learner.

        年龄（应当是计算字段）  # noqa: E501

        :return: The age of this Learner.
        :rtype: float
        """
        return self._age

    @age.setter
    def age(self, age: float):
        """Sets the age of this Learner.

        年龄（应当是计算字段）  # noqa: E501

        :param age: The age of this Learner.
        :type age: float
        """

        self._age = age

    @property
    def status(self) -> str:
        """Gets the status of this Learner.

        目前状态，包括在读、在读（游学）、在读（试读）、毕业、导师等；考虑是否需要更换成integer  # noqa: E501

        :return: The status of this Learner.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status: str):
        """Sets the status of this Learner.

        目前状态，包括在读、在读（游学）、在读（试读）、毕业、导师等；考虑是否需要更换成integer  # noqa: E501

        :param status: The status of this Learner.
        :type status: str
        """

        self._status = status

    @property
    def main_personal_id_type(self) -> str:
        """Gets the main_personal_id_type of this Learner.

        证件类型  # noqa: E501

        :return: The main_personal_id_type of this Learner.
        :rtype: str
        """
        return self._main_personal_id_type

    @main_personal_id_type.setter
    def main_personal_id_type(self, main_personal_id_type: str):
        """Sets the main_personal_id_type of this Learner.

        证件类型  # noqa: E501

        :param main_personal_id_type: The main_personal_id_type of this Learner.
        :type main_personal_id_type: str
        """

        self._main_personal_id_type = main_personal_id_type

    @property
    def main_personal_id(self) -> str:
        """Gets the main_personal_id of this Learner.

        证件号码  # noqa: E501

        :return: The main_personal_id of this Learner.
        :rtype: str
        """
        return self._main_personal_id

    @main_personal_id.setter
    def main_personal_id(self, main_personal_id: str):
        """Sets the main_personal_id of this Learner.

        证件号码  # noqa: E501

        :param main_personal_id: The main_personal_id of this Learner.
        :type main_personal_id: str
        """

        self._main_personal_id = main_personal_id

    @property
    def date_of_registration(self) -> str:
        """Gets the date_of_registration of this Learner.

        加入时间  # noqa: E501

        :return: The date_of_registration of this Learner.
        :rtype: str
        """
        return self._date_of_registration

    @date_of_registration.setter
    def date_of_registration(self, date_of_registration: str):
        """Sets the date_of_registration of this Learner.

        加入时间  # noqa: E501

        :param date_of_registration: The date_of_registration of this Learner.
        :type date_of_registration: str
        """

        self._date_of_registration = date_of_registration

    @property
    def reason_of_registration(self) -> str:
        """Gets the reason_of_registration of this Learner.

        加入原因  # noqa: E501

        :return: The reason_of_registration of this Learner.
        :rtype: str
        """
        return self._reason_of_registration

    @reason_of_registration.setter
    def reason_of_registration(self, reason_of_registration: str):
        """Sets the reason_of_registration of this Learner.

        加入原因  # noqa: E501

        :param reason_of_registration: The reason_of_registration of this Learner.
        :type reason_of_registration: str
        """

        self._reason_of_registration = reason_of_registration

    @property
    def previous_status(self) -> str:
        """Gets the previous_status of this Learner.

        加入前状态  # noqa: E501

        :return: The previous_status of this Learner.
        :rtype: str
        """
        return self._previous_status

    @previous_status.setter
    def previous_status(self, previous_status: str):
        """Sets the previous_status of this Learner.

        加入前状态  # noqa: E501

        :param previous_status: The previous_status of this Learner.
        :type previous_status: str
        """

        self._previous_status = previous_status

    @property
    def date_of_leave(self) -> str:
        """Gets the date_of_leave of this Learner.

        离开时间  # noqa: E501

        :return: The date_of_leave of this Learner.
        :rtype: str
        """
        return self._date_of_leave

    @date_of_leave.setter
    def date_of_leave(self, date_of_leave: str):
        """Sets the date_of_leave of this Learner.

        离开时间  # noqa: E501

        :param date_of_leave: The date_of_leave of this Learner.
        :type date_of_leave: str
        """

        self._date_of_leave = date_of_leave

    @property
    def reason_of_leave(self) -> str:
        """Gets the reason_of_leave of this Learner.

        离开原因  # noqa: E501

        :return: The reason_of_leave of this Learner.
        :rtype: str
        """
        return self._reason_of_leave

    @reason_of_leave.setter
    def reason_of_leave(self, reason_of_leave: str):
        """Sets the reason_of_leave of this Learner.

        离开原因  # noqa: E501

        :param reason_of_leave: The reason_of_leave of this Learner.
        :type reason_of_leave: str
        """

        self._reason_of_leave = reason_of_leave

    @property
    def destination_of_leave(self) -> str:
        """Gets the destination_of_leave of this Learner.

        下阶段目的地  # noqa: E501

        :return: The destination_of_leave of this Learner.
        :rtype: str
        """
        return self._destination_of_leave

    @destination_of_leave.setter
    def destination_of_leave(self, destination_of_leave: str):
        """Sets the destination_of_leave of this Learner.

        下阶段目的地  # noqa: E501

        :param destination_of_leave: The destination_of_leave of this Learner.
        :type destination_of_leave: str
        """

        self._destination_of_leave = destination_of_leave

    @property
    def mentorship(self) -> List[LearnerMentorship]:
        """Gets the mentorship of this Learner.

        导师关系  # noqa: E501

        :return: The mentorship of this Learner.
        :rtype: List[LearnerMentorship]
        """
        return self._mentorship

    @mentorship.setter
    def mentorship(self, mentorship: List[LearnerMentorship]):
        """Sets the mentorship of this Learner.

        导师关系  # noqa: E501

        :param mentorship: The mentorship of this Learner.
        :type mentorship: List[LearnerMentorship]
        """

        self._mentorship = mentorship

    @property
    def salary_card(self) -> str:
        """Gets the salary_card of this Learner.

        工资卡号  # noqa: E501

        :return: The salary_card of this Learner.
        :rtype: str
        """
        return self._salary_card

    @salary_card.setter
    def salary_card(self, salary_card: str):
        """Sets the salary_card of this Learner.

        工资卡号  # noqa: E501

        :param salary_card: The salary_card of this Learner.
        :type salary_card: str
        """

        self._salary_card = salary_card

    @property
    def custodian_info(self) -> List[LearnerCustodianInfo]:
        """Gets the custodian_info of this Learner.

        监护人信息  # noqa: E501

        :return: The custodian_info of this Learner.
        :rtype: List[LearnerCustodianInfo]
        """
        return self._custodian_info

    @custodian_info.setter
    def custodian_info(self, custodian_info: List[LearnerCustodianInfo]):
        """Sets the custodian_info of this Learner.

        监护人信息  # noqa: E501

        :param custodian_info: The custodian_info of this Learner.
        :type custodian_info: List[LearnerCustodianInfo]
        """

        self._custodian_info = custodian_info

    @property
    def emergent_contact(self) -> List[LearnerEmergentContact]:
        """Gets the emergent_contact of this Learner.

        紧急联系人  # noqa: E501

        :return: The emergent_contact of this Learner.
        :rtype: List[LearnerEmergentContact]
        """
        return self._emergent_contact

    @emergent_contact.setter
    def emergent_contact(self, emergent_contact: List[LearnerEmergentContact]):
        """Sets the emergent_contact of this Learner.

        紧急联系人  # noqa: E501

        :param emergent_contact: The emergent_contact of this Learner.
        :type emergent_contact: List[LearnerEmergentContact]
        """

        self._emergent_contact = emergent_contact

    @property
    def contact_info(self) -> LearnerContactInfo:
        """Gets the contact_info of this Learner.


        :return: The contact_info of this Learner.
        :rtype: LearnerContactInfo
        """
        return self._contact_info

    @contact_info.setter
    def contact_info(self, contact_info: LearnerContactInfo):
        """Sets the contact_info of this Learner.


        :param contact_info: The contact_info of this Learner.
        :type contact_info: LearnerContactInfo
        """

        self._contact_info = contact_info

    @property
    def medical_info(self) -> LearnerMedicalInfo:
        """Gets the medical_info of this Learner.


        :return: The medical_info of this Learner.
        :rtype: LearnerMedicalInfo
        """
        return self._medical_info

    @medical_info.setter
    def medical_info(self, medical_info: LearnerMedicalInfo):
        """Sets the medical_info of this Learner.


        :param medical_info: The medical_info of this Learner.
        :type medical_info: LearnerMedicalInfo
        """

        self._medical_info = medical_info

    @property
    def notes(self) -> List[str]:
        """Gets the notes of this Learner.

        备注  # noqa: E501

        :return: The notes of this Learner.
        :rtype: List[str]
        """
        return self._notes

    @notes.setter
    def notes(self, notes: List[str]):
        """Sets the notes of this Learner.

        备注  # noqa: E501

        :param notes: The notes of this Learner.
        :type notes: List[str]
        """

        self._notes = notes
