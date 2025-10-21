import sys

class Coordinate:
    _MAX: float = 90.0
    _MIN: float = -90.0

    def __init__(self, str_value: str):
        try:
            self.validate_coordinate(str_value)
        except ValueError as e:
            raise SystemExit(f"The value must be numeric and in range {self._MIN}< X <={self._MAX}") from e
        self._value = float(str_value)

    def validate_coordinate(self, str_value: str):
        try:
            float_value = float(str_value)
        except ValueError as e:
            raise ValueError(f"Invalid input data: {e}") from e
        if float_value <= self._MIN or float_value > self._MAX:
            raise ValueError(f"{self.__class__.__name__} not in range {self._MIN}< X <={self._MAX}")
        return True
    
    def __str__(self):
        return str(self._value)
    
    def __eq__(self, other: float) -> bool:
        return other == self._value
    
    def __ne__(self, other: float) -> bool:
        return other != self._value

    def __lt__(self, other: float) -> bool:
        return self._value < other

    def __le__(self, other: float) -> bool:
        return self._value < other or self._value == other

    def __gt__(self, other: float) -> bool:
        return self._value > other

    def __ge__(self, other: float) -> bool:
        return self._value > other or self._value == other

    @property
    def min(self):
        return self._MIN

    @property
    def max(self):
        return self._MAX

class Latitude(Coordinate):
    pass

class Longitude(Coordinate):
    _MAX = 180.0
    _MIN = -180.0

class Geohash:
    _CHUNK_SIZE = 5
    _ENCODED_SIZE = 32
    _HASHTABLE = (
        '0', '1', '2', '3', '4', '5', '6', '7',
        '8', '9', 'b', 'c', 'd', 'e', 'f', 'g',
        'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r',
        's', 't', 'u', 'v', 'w', 'x', 'y', 'z')

    def __init__(self):
        if (2 ** self._CHUNK_SIZE) > len(self._HASHTABLE):
            raise ValueError("Geohash._CHUNK_SIZE max possible value can not be greather than len(Geohash._HASHTABLE)")
        
    @staticmethod
    def _interleave_coordinates(xbin: str, ybin: str):
        final_bin = "".join([bit1 + bit2 for bit1, bit2 in zip(xbin, ybin)])
        return final_bin

    @staticmethod
    def split_string_into_chunks(input_string: str, chunk_size: int):
        splited: list[str] = [input_string[i:i + chunk_size] for i in range(0, len(input_string), chunk_size)]
        if len(input_string) % chunk_size != 0:
            return splited[: -1]
        return splited

    @classmethod
    def _encode_coordinate(cls, coordinate: Coordinate) -> str:
        interval = {
            'min': coordinate.min,
            'max': coordinate.max,
            'mid': 0.0
        }
        bin32: list[str] = [""] * cls._ENCODED_SIZE
        for i in range(cls._ENCODED_SIZE):
            if coordinate >= interval['mid']:
                bin32[i] = '1'
                interval['min'] = interval['mid']
            else:
                bin32[i] = '0'
                interval['max'] = interval['mid']
            interval['mid'] = (interval['max'] + interval['min']) / 2
        return "".join(bin32)


    @classmethod
    def _hash_chunks(cls, chunks: list[str]):
        return [cls._hash(int(chunk, base=2)) for chunk in chunks]

    @classmethod
    def _hash(cls, to_hash: int):
        return cls._HASHTABLE[to_hash]

    def generate_hash(self, latitude: Latitude, longitude: Longitude):
        encoded_latitude = self._encode_coordinate(latitude)
        encoded_longitude = self._encode_coordinate(longitude)
        interleaved = self._interleave_coordinates(encoded_latitude, encoded_longitude)
        encoded_chunks = self.split_string_into_chunks(interleaved, self._CHUNK_SIZE)
        hashed_chunkes = self._hash_chunks(encoded_chunks)
        return "".join(hashed_chunkes)

if __name__ == "__main__":
    EXPECTED_ARGC = 2
    if (argc := len(sys.argv) - 1) != EXPECTED_ARGC:
        raise SystemExit(f"takes {EXPECTED_ARGC} positional arguments <latitude> <longitude>, given {argc}")
    latitude = Latitude(sys.argv[1])
    longitude = Longitude(sys.argv[2])

    print(latitude, longitude)

    geohashing = Geohash()

    position_hash = geohashing.generate_hash(latitude, longitude)
    print(position_hash)

