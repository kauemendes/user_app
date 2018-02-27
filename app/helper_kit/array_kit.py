

class ArrayKit:

    @staticmethod
    def append_string_to_values(values, append, prepend):
        result = []

        for value in values:
            result.append(prepend + str(value) + append)

        return result

    @staticmethod
    def get_item_or_none(values: list, index: int):
        if values is None:
            return None

        if index > len(values) - 1:
            return None

        return values[index]
