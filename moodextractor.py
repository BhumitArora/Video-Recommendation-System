import pandas as pd


def extract_moods(post_summary):
    # Check if 'post_summary' is a dictionary
    if isinstance(post_summary, dict):
        # Case 1: 'emotions' is a list
        if 'emotions' in post_summary and isinstance(post_summary['emotions'], list):
            return post_summary['emotions']
        # Case 2: 'emotions' is a dictionary with arbitrary keys
        elif 'emotions' in post_summary and isinstance(post_summary['emotions'], dict):
            # Combine all values from the 'emotions' dictionary
            all_emotions = []
            for key, value in post_summary['emotions'].items():
                if isinstance(value, list):  # Ensure values are lists before extending
                    all_emotions.extend(value)
                elif isinstance(value, str):  # Include string values directly
                    all_emotions.append(value)
            return all_emotions
    # If structure is unexpected or 'post_summary' is not a dictionary
    return []