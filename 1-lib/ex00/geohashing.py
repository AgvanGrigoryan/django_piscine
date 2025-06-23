import sys
import antigravity

if __name__ == "__main__":
    if argc := len(sys.argv) != 5:
        raise SystemExit(f"takes 3 positional arguments [latitude, longitude, date(YYY-MM-DD), dow], given {argc}")
    
    try:
        latitude = float(sys.argv[1])
        longitude = float(sys.argv[2])
    except ValueError as e:
        raise SystemExit("Invalid input data") from e
    date = sys.argv[3]
    dow = sys.argv[4]
    geohash_str = f"{date}-{dow}"
    antigravity.geohash(latitude, longitude, geohash_str.encode())