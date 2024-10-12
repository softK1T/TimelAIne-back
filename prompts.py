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
        "real": "close to reality"
    }

    brutality = {
        "brutal": "brutal",
        "light": "light",
        "sfw": "safe",
        "most_brutal": "the most brutal in the world",
        "hell": "the world is in a literal hell"
    }

    detailed = "Add detailed information for each event (up to 400 characters). Add a detailed information about the conflicts that are now active (can exceed characters limit)" if isDetailed else ''

    population = "Provide Earth's population at the time of each event, rounded to two decimals and use units (k, m, b)" if isPopulation else ''

    prompts: Dict[str, str] = {
        PromptType.DEFAULT: f"""
            Create an alternative global timeline featuring the event: '{message}'.
            Identify 5 key global events that are likely to occur, with specific dates.
            Timeline must be {reality[reality_type]}.
            Story must be {brutality[brutality_type]}.

            **Format:** JSON string

            **Instructions:**
            0. CREATE EVENTS ONLY ABOUT THE MAIN EVENT 
            1. Each event must be concise, a maximum of 150 characters.
            2. Include an emojis (up to 3) for each event.
            3. Use only the event language in your response.
            4. Use the communicating style the same as the message style (official or non-official).
            5. The storyline should be tied together with logical connections.
            6. Emojis must only be included in the emojis field, dates only in dates field
            7. Include the most interesting information (write about countries, cities)
            {detailed}
            {population}
            **Example JSON structure:**
            [            {{                "evt": "Global Event Occurs",                "dt": "YYYY-MM-DD",                "emj": "🔍",                "dtl": "Detailed description of the event."(if included in instructions),                "pop": "X.XXb"(if included in instructions)            }}        ]
        """,
        PromptType.CONTINUE: (f"""
            Continue the story in the same format from the year you ended. 
            "All events must be logically connected, including population info. 
            "Use the same language provided here.
            ** Instructions: **
            1. Each event must be concise, a maximum of 150 characters.
            2. Include an emojis (up to 3) for each event.
            3. Use the message language in your response.
            4. Use the communicating style the same as the message style (official or non-official).
            5. The storyline should be tied together with logical connections.
            6. Emojis must only be included in the emojis field, dates only in dates field
            7. Include the most interesting information (write about countries, cities)
            {detailed}
            {population}
            ** Example JSON structure:**
            [{{"evt": "Global Event Occurs", "dt": "YYYY-MM-DD", "emj": "🔍", "dtl": "Detailed description of the event.",
           "pop": "X.XXb"}}]
           Main event: {message}
    """
                              )
    }
    # Return the requested prompt type or fall back to the default
    return prompts.get(prompt_type, prompts[PromptType.DEFAULT])
