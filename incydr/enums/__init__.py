import enum


class Enum(str, enum.Enum):
    """
    An `enum.Enum` subclass that enables string comparison (`Enum.MEMBER == "MEMBER"`) and better exceptions that show
    all possible values.
    """

    @classmethod
    def _missing_(cls, value):
        if value in cls.__members__:
            return None
        raise ValueError(
            f"'{value}' is not a valid {cls.__module__}.{cls.__name__}. Expected one of {[member.value for member in cls]}"
        )


class SrtDir(Enum):
    ASC = "asc"
    DESC = "desc"