from typing import List, Dict


# Define the PromptType
class PromptType:
    DEFAULT = "default"
    CONTINUE = "continue"


# Define the Event data structure
class Event:
    def __init__(self, emj: str, dt: str, evt: str):
        self.emj = emj  # Emoji representation
        self.dt = dt  # Date of the event
        self.evt = evt  # Description of the event


# Function to create prompts
def call_prompt(message: str, reality_type: str, brutality_type: str, isDetailed: bool, isPopulation: bool,
                prompt_type: str = PromptType.DEFAULT) -> str:
    reality = {
        "unreal": "unreal and just interesting to read, imagine something very uncommon",
        "real": "close to reality",
    }

    brutality = {
        "brutal": "brutal",
        "light": "light",
        "sfw": "safe",
        "most_brutal": "the most brutal in the world",
        "hell": "the world is in a literal hell"
    }
    detailed = "Provide me detailed information to each event as a new key-value pair (400 characters) dtl: details " if isDetailed else ''
    population = "Provide me number of population of Earth to each event as a new key-value pair (format: rounded value to 2 decimals and literal k, m, b etc) ) pop: population " if isPopulation else ''
    prompts: Dict[str, str] = {
        PromptType.DEFAULT: (
            f"Create an alternative timeline. Event: {message}. "
            "Give 5 key global events likely to occur and their dates. "
            f"Timeline must be {reality[reality_type]}. Key events should be max 150 characters and logically connected. "
            f"Story must be {brutality[brutality_type]}. "
            "Include emojis for each event. "
            "Format: JSON string. STRICT! No excessive words! Use the language provided. "
            "[{evt: event, dt: date, emj: emoji }, ...] "
            f"{detailed}{population}"
        ),        PromptType.CONTINUE: "Continue the story in the same format from the year you ended. (Use the language provided here). All the events must be logically connected, as well as population [{evt: event, dt: date, emj: emoji }",
    }

    # Return the requested prompt type or fall back to the default
    return prompts.get(prompt_type, prompts[PromptType.DEFAULT])
