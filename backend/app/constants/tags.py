# app/constants/tags.py

# --- Define Tag Categories (Static Data) ---
# These IDs will correspond to the 'id' column in your tag_categories table.
CATEGORY_IDS = {
    "HOBBIES": 1,
    "FOOD": 2,
    "PERSONALITY": 3,
    "FITNESS": 4,
    "MUSIC": 5
}

# --- Define Tags and their Category ---
# This structure helps validation and ensures all tags belong to a valid category.
ALL_TAGS = {
    # HOBBIES (CATEGORY_IDS["HOBBIES"] = 1)
    "Gaming": 1,
    "Reading": 1,
    "Traveling": 1,
    "Photography": 1,
    
    # FOOD (CATEGORY_IDS["FOOD"] = 2)
    "Vegan": 2,
    "Keto": 2,
    "Coffee Lover": 2,
    "Chef": 2,
    
    # PERSONALITY (CATEGORY_IDS["PERSONALITY"] = 3)
    "Introvert": 3,
    "Extrovert": 3,
    "Geek": 3,
    "Sarcastic": 3,
    
    # FITNESS (CATEGORY_IDS["FITNESS"] = 4)
    "Gym Rat": 4,
    "Yoga": 4,
    "Running": 4,
    
    # MUSIC (CATEGORY_IDS["MUSIC"] = 5)
    "Hip Hop": 5,
    "Classical": 5,
    "Indie": 5,
}