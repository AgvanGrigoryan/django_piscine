import sys

def get_states() -> dict[str, str]:
	states = {
		"Oregon" : "OR",
		"Alabama" : "AL",
		"New Jersey": "NJ",
		"Colorado" : "CO"
	}
	return states

def get_capital_cities() -> dict[str, str]:
	capital_cities = {
		"OR": "Salem",
		"AL": "Montgomery",
		"NJ": "Trenton",
		"CO": "Denver"
	}
	return capital_cities

def get_key_by_value(d: dict[str, str], target_value: str | None) -> str | None:
	# print("\nA", target_value)
	if target_value is None:
		return None
	for key, value in d.items():
		# print(key, value)
		if value == target_value:
			return key
	return None

if __name__ == "__main__":
	EXPECTED_ARGC = 2
	if len(sys.argv) != EXPECTED_ARGC:
		exit(1)
	target_capital : str = sys.argv[1]
	states : dict[str, str] = get_states()
	capital_cities : dict[str, str] = get_capital_cities()
	state_code : str | None = get_key_by_value(capital_cities, target_capital)
	state : str | None = get_key_by_value(states, state_code)
	if state is None:
		print("Unknown capital city")
	else:
		print(state)

	
