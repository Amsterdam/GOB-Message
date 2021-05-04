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
    def _parse_incomplete_date(value: str) -> str:
        year, month, day = value[:4], value[4:6], value[6:8]

        if year == '0000' and month == '00' and day == '00':
            d = f'0000-00-00'
        elif month == '00' and day == '00':
            d = datetime.datetime.strptime(year, "%Y")
            d = d.strftime("%Y-00-00")
        elif day == '00':
            d = datetime.datetime.strptime(year + month, "%Y%m")
            d = d.strftime("%Y-%m-00")
        else:
            raise ValueError(f"Can not parse incomplete date: '{value}'")

        return d

    @staticmethod
    def to_incomplete_date(value: str):
        """
        De mogelijke waarden van (incomplete) datum zijn:
         - jjjjmmdd volledige datum
         - jjjjmm00 dag onbekend
         - jjjj0000 maand onbekend
         - 00000000 datum onbekend

        :param value: string
        :return:
        """
        if value is None:
            return None

        try:
            date = ValueConverter.to_date(value)
        except ValueError:
            date = ValueConverter._parse_incomplete_date(value)

        return date

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

    @staticmethod
    def concat(char: str):
        def converter(*values):
            return char.join(values)
        return converter

    @staticmethod
    def _filter_aot(identifier: str, type_digits: str):
        """Filter AOT based on the two type_digits; only returns value if the 5th and 6th position of
        the identifier match type_digits

        :param value:
        :param digits:
        :return:
        """
        return identifier if identifier and len(identifier) > 5 and identifier[4:6] == type_digits else None

    @staticmethod
    def filter_vot(value: str):
        return ValueConverter._filter_aot(value, '01')

    @staticmethod
    def filter_lps(value: str):
        return ValueConverter._filter_aot(value, '02')

    @staticmethod
    def filter_sps(value: str):
        return ValueConverter._filter_aot(value, '03')
