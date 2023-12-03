'''
style_sheet.py : Module
Provides Formatting Information for the project 
'''


COLORS = {
    "MONEY_GREEN" : "#5B8469",      # Background Color
    "DARK_MONEY_GREEN": "#102315",  # Seconddary Color
    "HIGHLIGHT_YELLOW" : "#EEE8CD", # Primary Color
    "ACCENT_GOLD" : "#f0cb26",      # Accent Color
    "TEXT_WHITE" : "#ffffff",       # White Text for Dark Background
    "TEXT_BLACK" : "#000000",       # Black Text for bright Background 
}



H1 = { #For Category Labels
    "FONT": ("Euphemia", 25, "bold"),
    "FONT_COLOR": COLORS["TEXT_WHITE"],
    "BACKGROUND_COLOR": COLORS["DARK_MONEY_GREEN"]
}

H2 = {
    "FONT": ("Euphemia", 17, "bold"),
    "FONT_COLOR": COLORS["TEXT_WHITE"],
    "BACKGROUND_COLOR": COLORS["DARK_MONEY_GREEN"]
}

QUESTION_CARD = {
    "FONT": ("Euphemia", 30, "bold"),
    "FONT_COLOR": COLORS["ACCENT_GOLD"],
    "BACKGROUND_COLOR": COLORS["DARK_MONEY_GREEN"]
}


BID_CARD  = {
    "FONT": ("Euphemia", 25),
    "FONT_COLOR": COLORS["ACCENT_GOLD"],
    "BACKGROUND_COLOR": COLORS["DARK_MONEY_GREEN"]
}

REGULAR_TEXT = {
    "FONT": ("Euphemia", 15),
    "FONT_COLOR": COLORS["HIGHLIGHT_YELLOW"],
    "BACKGROUND_COLOR": COLORS["MONEY_GREEN"]
}

OPTION_BUTTONS = {
    "FONT": ("Euphemia", 13),
    "FONT_COLOR": COLORS["TEXT_BLACK"],
    "BACKGROUND_COLOR": COLORS["HIGHLIGHT_YELLOW"]
}

PRIMARY_BUTTON = {
    "FONT": ("Euphemia", 20, "bold"),
    "FONT_COLOR": COLORS["TEXT_WHITE"],
    "BACKGROUND_COLOR": COLORS["DARK_MONEY_GREEN"]
}

