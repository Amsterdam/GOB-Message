import datetime


class ValueConverter:
    @staticmethod
    def jn_to_bool(value: str):
        if value == 'J':
            return True
        if value == 'N':
            return False
        return None

    @staticmethod
    def to_date(value: str):
        """

        :param value: string of the form yyyymmdd
        :return:
        """
        if value is None:
            return None
        d = datetime.datetime.strptime(value, "%Y%m%d")
        return d.strftime("%Y-%m-%d")

    @staticmethod
    def to_datetime(value: str):
        """

        :param value: string of the form yyyymmddhhmmssmmm
        :return:
        """
        if value is None:
            return None
        d = datetime.datetime.strptime(value, "%Y%m%d%H%M%S%f")
        return d.isoformat()
