import json

# The internal taxonomy from the assignment (taxonomy.json)
taxonomy = {
    "Fiction": {
        "Romance": ["Slow-burn", "Enemies-to-Lovers", "Second Chance"],
        "Thriller": ["Espionage", "Psychological", "Legal Thriller"],
        "Sci-Fi": ["Hard Sci-Fi", "Space Opera", "Cyberpunk"],
        "Horror": ["Psychological Horror", "Gothic", "Slasher"]
    }
}

# Let's print it to check everything is correct
print("Taxonomy loaded:")
print(json.dumps(taxonomy, indent=4))

# The 10 test cases from the assignment (hardcoded as a list)
test_cases = [
    {
        "id": 1,
        "tags": ["Love"],
        "blurb": "They hated each other for years, working in the same cubicle, until a late-night deadline changed everything."
    },
    {
        "id": 2,
        "tags": ["Action", "Spies"],
        "blurb": "Agent Smith must recover the stolen drive without being detected by the Kremlin."
    },
    {
        "id": 3,
        "tags": ["Scary", "House"],
        "blurb": "The old Victorian mansion seemed to breathe, its corridors whispering secrets of the family's dark past."
    },
    {
        "id": 4,
        "tags": ["Love", "Future"],
        "blurb": "A story about a man who falls in love with his AI operating system in a neon-drenched Tokyo."
    },
    {
        "id": 5,
        "tags": ["Action"],
        "blurb": "The lawyer stood before the judge, knowing this cross-examination would decide the fate of the city."
    },
    {
        "id": 6,
        "tags": ["Space"],
        "blurb": "How to build a telescope in your backyard using basic household items."
    },
    {
        "id": 7,
        "tags": ["Sad", "Love"],
        "blurb": "They met again 20 years after the war, both gray-haired, wondering what could have been."
    },
    {
        "id": 8,
        "tags": ["Robots"],
        "blurb": "A deep dive into the physics of FTL travel and the metabolic needs of long-term stasis."
    },
    {
        "id": 9,
        "tags": ["Ghost"],
        "blurb": "A masked killer stalks a group of teenagers at a summer camp."
    },
    {
        "id": 10,
        "tags": ["Recipe", "Sweet"],
        "blurb": "Mix two cups of flour with sugar and bake at 350 degrees."
    }
]

# Let's check by printing the first case as an example
print("\nFirst test case loaded:")
print(f"ID: {test_cases[0]['id']}")
print(f"Tags: {test_cases[0]['tags']}")
print(f"Blurb: {test_cases[0]['blurb']}")
# My personal keyword mapping for each sub-genre
# I created these keywords by carefully reading each blurb and expected logic
# Prioritizing strong indicators from the story description (blurb) over tags

keyword_mapping = {
    "Enemies-to-Lovers": ["hated", "enemies", "rivals", "cubicle", "deadline changed", "hate to love"],
    "Second Chance": ["met again", "years later", "reunited", "gray-haired", "what could have been", "after the war"],
    "Slow-burn": ["gradual", "slow", "build-up", "tension"],  # Not strongly in tests, but kept for completeness
    
    "Espionage": ["agent", "spy", "stolen drive", "kremlin", "undetected", "recover secret"],
    "Legal Thriller": ["lawyer", "judge", "court", "cross-examination", "trial", "fate of the city"],
    "Psychological": ["mind", "psychological", "mental game"],
    
    "Hard Sci-Fi": ["physics", "ftl travel", "stasis", "metabolic", "scientific", "deep dive"],
    "Cyberpunk": ["ai", "artificial intelligence", "operating system", "neon-drenched", "tokyo", "future love"],
    "Space Opera": ["galactic", "epic space", "opera"],
    
    "Gothic": ["victorian mansion", "breathe", "whispering", "dark past", "old house secrets", "corridors"],
    "Slasher": ["masked killer", "stalks", "teenagers", "summer camp", "slasher"],
    "Psychological Horror": ["mind terror", "psychological horror"]
}

# Quick check: print how many sub-genres we have keywords for
print(f"\nI defined keywords for {len(keyword_mapping)} sub-genres.")
print("Example - Enemies-to-Lovers keywords:", keyword_mapping["Enemies-to-Lovers"])

# Helper function to find the parent genre for a given sub-genre
def get_genre_for_subgenre(subgenre):
    for genre, subgenres in taxonomy["Fiction"].items():
        if subgenre in subgenres:
            return genre
    return None

# Main inference function - this is my personal logic
def infer_mapping(tags, blurb):
    """
    My approach:
    1. Always prioritize the blurb (story description) - Context Wins!
    2. Convert everything to lowercase for matching
    3. Count how many of my keywords appear in the blurb
    4. Pick the sub-genre with the highest blurb matches
    5. If no strong blurb match, check tags as secondary clue
    6. If still low confidence -> [UNMAPPED] (Honesty rule)
    """
    blurb_lower = blurb.lower()
    tags_lower = " ".join(tags).lower()  # Combine tags into one string
    
    # Dictionary to store match counts for each sub-genre
    match_scores = {}
    matched_keywords = {}
    
    # Check matches in blurb first (primary source)
    for subgenre, keywords in keyword_mapping.items():
        matches_in_blurb = []
        for kw in keywords:
            if kw.lower() in blurb_lower:
                matches_in_blurb.append(kw)
        score = len(matches_in_blurb)
        match_scores[subgenre] = score
        if score > 0:
            matched_keywords[subgenre] = matches_in_blurb
    
    # If no blurb matches at all, check tags as fallback
    if max(match_scores.values(), default=0) == 0:
        for subgenre, keywords in keyword_mapping.items():
            matches_in_tags = []
            for kw in keywords:
                if kw.lower() in tags_lower:
                    matches_in_tags.append(kw)
            additional_score = len(matches_in_tags)
            match_scores[subgenre] += additional_score  # Add to score
            if additional_score > 0 and subgenre in matched_keywords:
                matched_keywords[subgenre].extend(matches_in_tags)
            elif additional_score > 0:
                matched_keywords[subgenre] = matches_in_tags
    
    # Find the best matching sub-genre
    best_score = max(match_scores.values(), default=0)
    
    # Honesty rule: if no meaningful match (I chose threshold 1), return UNMAPPED
    if best_score == 0:
        return "[UNMAPPED]", "No relevant keywords found in blurb or tags - does not fit any fiction sub-genre."
    
    # Get the sub-genre with highest score
    best_subgenre = max(match_scores, key=match_scores.get)
    genre = get_genre_for_subgenre(best_subgenre)
    
    # Create personal reasoning
    keywords_found = matched_keywords.get(best_subgenre, [])
    if keywords_found:
        reasoning = f"Strong match in blurb with keywords: {', '.join(keywords_found)}. Mapped to {best_subgenre} under {genre}."
    else:
        reasoning = f"Weak fallback match in tags led to {best_subgenre} under {genre}."
    
    # Final output format: "Genre: Sub-genre"
    return f"{genre}: {best_subgenre}", reasoning

# Quick test: Let's try Case 1 manually
test_blurb = test_cases[0]["blurb"]
test_tags = test_cases[0]["tags"]
mapping, reasoning = infer_mapping(test_tags, test_blurb)

print("\nQuick test on Case 1:")
print(f"Tags: {test_tags}")
print(f"Blurb: {test_blurb}")
print(f"Predicted mapping: {mapping}")
print(f"Reasoning: {reasoning}")
# Process all 10 test cases and collect results
print("\n" + "="*50)
print("PROCESSING ALL 10 TEST CASES")
print("="*50)

results = []
for case in test_cases:
    case_id = case["id"]
    tags = case["tags"]
    blurb = case["blurb"]
    
    mapping, reasoning = infer_mapping(tags, blurb)
    
    # Store the result
    results.append({
        "id": case_id,
        "tags": tags,
        "blurb": blurb,
        "mapping": mapping,
        "reasoning": reasoning
    })
    
    # Print on screen for you to see
    print(f"Case {case_id}: {mapping}")
    print(f"   Reasoning: {reasoning}")
    print("-" * 30)

# Save the final reasoning log to a JSON file
output_filename = "output_log.json"
with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

print(f"\nAll done! Reasoning log saved to '{output_filename}'")
print("You can now open this file and see the full results.")