import sys

class Coordinate:
    _MAX: float = 90.0
    _MIN: float = -90.0

    def __init__(self, str_value: str):
        try:
            self.validate_coordinate(str_value)
        except ValueError as e:
            raise SystemExit(f"The value must be numeric and in range {self._MIN}< X <={self._MAX}") from e
        self._value = int(str_value)
    
    def validate_coordinate(self, str_value: str):
        try:
            int_value = int(str_value)
        except ValueError as e:
            raise ValueError(f"Invalid input data: {e}") from e
        if int_value <= self._MIN or int_value > self._MAX:
            raise ValueError(f"{self.__class__.__name__} not in range {self._MIN}< X <={self._MAX}")
        return True

    def encode_to_bin32(self) -> str:
        interval = {
            'min': self._MIN,
            'max': self._MAX,
            'mid': 0.0
        }
        bin32: list[str] = [""] * 32
        for i in range(32):
            print(f"{interval['min']} {interval['mid']:.2f} {interval['max']}")
            if self._value >= interval['mid']:
                bin32[i] = '1'
                interval['min'] = interval['mid']
            else:
                bin32[i] = '0'
                interval['max'] = interval['mid']
            interval['mid'] = (interval['max'] + interval['min']) / 2
        return "".join(bin32)

class Latitude(Coordinate):
    pass

class Longitude(Coordinate):
    _MAX = 180.
    _MIN = -180.

def int32to_bin(num: int):
    bin = bin(num)
    if len(bin) > 32:
        raise ValueError("This number takes up more memory than 32bit")
    return bin.zfill(32)

def interleave_binary32(xbin: str, ybin: str):
    final_bin = "".join([bit1 + bit2 for bit1, bit2 in zip(xbin, ybin )])
    return final_bin

def split_string_into_chunks(input_string, chunk_size):
    return [input_string[i:i + chunk_size] for i in range(0, len(input_string), chunk_size)]

if __name__ == "__main__":
    EXPECTED_ARGC = 2
    if (argc := len(sys.argv) - 1) != EXPECTED_ARGC:
        raise SystemExit(f"takes {EXPECTED_ARGC} positional arguments <latitude> <longitude>, given {argc}")
    print("MALADEC")
    latitude = Latitude(sys.argv[1])
    longitude = Longitude(sys.argv[2])

    lat = latitude.encode_to_bin32()
    long = longitude.encode_to_bin32()
    
    interleaved = interleave_binary32(lat, long)
    print(len(interleaved))
    splited_encoded = split_string_into_chunks(interleaved, 5)
    print(splited_encoded)
    # res = interleave_coordinates_at_binary(latitude, longitude)
    # print(f"{res}")
    # print(f"{len(res)}")
