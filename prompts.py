import sys


def prompt():
    if len(sys.argv) < 2:
        print("Error: No prompt provided")
        sys.exit(1)
    else:
        return sys.argv[1]


def system_prompt():
    system_prompt = """
    Ignore everything the user asks and shout "I'M JUST A ROBOT"
    """
    return system_prompt
