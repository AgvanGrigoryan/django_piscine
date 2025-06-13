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

def process(target_state: str) -> None:
	states : dict[str, str] = get_states()
	capital_cities : dict[str, str] = get_capital_cities()
	state_code : str | None = states.get(target_state)
	if state_code is not None:
		print(capital_cities.get(state_code, "Unknown state"))
	else:
		print("Unknown state")

if __name__ == "__main__":
	EXPECTED_ARGC = 2
	if len(sys.argv) != EXPECTED_ARGC:
		exit(1)
	process(sys.argv[1])
	