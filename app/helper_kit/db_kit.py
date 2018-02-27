from app.helper_kit.string_kit import StringKit
from app.models.enums import ProcessTypeNames


class DBKit:

    @staticmethod
    def sanitize(value):
        return value

    @staticmethod
    def generate_filter_or_like(field, values):
        return DBKit.generate_filter_generic(field, values, "OR", True)

    @staticmethod
    def generate_filter_or_equal(field, values):
        return DBKit.generate_filter_generic(field, values, "OR", False)

    @staticmethod
    def generate_filter_generic(field, values, connector, use_like=False):
        result = ""
        dict_values = {}

        equal_connector = " LIKE " if use_like else " = "

        for i in range(len(values)):
            value_key = StringKit.random_key(10) + str(i)

            if use_like:
                dict_values[value_key] = "%" + values[i] + "%"
            else:
                dict_values[value_key] = values[i]

            result += ((" " + connector + " ") if i > 0 else " ") + field
            result += equal_connector + " :" + value_key + " "

        return result, dict_values

    @staticmethod
    def generate_filter_for_process_pending(process_pending):
        result = ""
        dict_values = {}

        for process in process_pending:
            value_key = StringKit.random_key(10) + str(process)

            if result != "":
                result += " OR "

            if process == ProcessTypeNames.PROCESS_REQUEST.value:
                result += " s.process_type_request =  :"+value_key
                dict_values[value_key] = 0
            if process == ProcessTypeNames.PROCESS_APPROVAL.value:
                result += " s.process_type_approval = :"+value_key
                dict_values[value_key] = 0
            if process == ProcessTypeNames.PROCESS_PRE_ANESTHETIC.value:
                result += " s.process_type_pre_anesthetic = :"+value_key
                dict_values[value_key] = 0
            if process == ProcessTypeNames.PROCESS_SCHEDULING.value:
                result += " s.process_type_scheduling = :"+value_key
                dict_values[value_key] = 0
            if process == ProcessTypeNames.PROCESS_POST_SURGICAL.value:
                result += " s.process_type_post_surgical = :"+value_key
                dict_values[value_key] = 0

        return result, dict_values
