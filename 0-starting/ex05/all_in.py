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
	if target_value is None:
		return None
	for key, value in d.items():
		if value == target_value:
			return key
	return None

def get_state_code(target: str, *, states: dict[str, str], capitals: dict[str, str]) -> str | None:
	first_state_code = states.get(target)
	second_state_code = get_key_by_value(capitals, target)
	if first_state_code is None and second_state_code is None:
		return None
	return first_state_code or second_state_code

def get_state_info(state_code: str, *, states: dict[str, str], capitals: dict[str, str]) -> dict[str, str] | None:
	capital = capitals.get(state_code)
	if capital is None:
		return None
	state = get_key_by_value(states, state_code)
	if state is None:
		return None
	return {"state": state, "capital": capital}

def process(args: list[str]) -> None:
	states : dict[str, str] = get_states()
	capital_cities : dict[str, str] = get_capital_cities()

	inputs = [arg.strip() for arg in args if arg.strip()]

	for name in inputs:
		state_info: dict[str, str] | None = None
		state_code: str | None = get_state_code(name.title(), states=states, capitals=capital_cities)
		
		if state_code is not None:
			state_info = get_state_info(state_code, states=states, capitals=capital_cities)
		if state_info is None:
			print(f"{name} is neither a capital city nor a state")
		else:
			print(f"{state_info['capital']} is the capital of {state_info['state']}")

if __name__ == "__main__":
	EXPECTED_ARGC = 2
	if len(sys.argv) != EXPECTED_ARGC:
		exit(0)
	process(sys.argv[1].split(','))
