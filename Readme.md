# Video Recommendation System

This project implements a video recommendation system that combines Collaborative Filtering (CF) and Content-Based Filtering (CBF) techniques to provide personalized video recommendations based on user preferences.

The system utilizes interaction data (e.g., user interactions with videos) and video content features (e.g., moods, categories) to generate recommendations. It leverages a hybrid approach to combine the strengths of both CF and CBF, improving the accuracy and relevance of the recommendations.

Key features:

Collaborative Filtering (CF): Generates recommendations based on user-item interactions.
Content-Based Filtering (CBF): Recommends videos based on similarities in video content features (moods, category, etc.).
Hybrid Approach: Combines CF and CBF to produce more accurate and personalized recommendations.
Scoring System: Ranks videos based on a weighted scoring formula considering factors like upvotes, views, and ratings.

# Project Setup Guide

## 1. Create a Virtual Environment

Follow the steps below to create a virtual environment for the project:

### On Windows:

1. Open your command prompt or PowerShell.
2. Navigate to the project directory.
3. Run the following command to create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

### On Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install Packages from requirements.txt:

   ```bash
   pip3 install -r requirements.txt
   ```

# Fetch the api data

The code related to the api is in api_fetcher.py in fetcher.
API links:
    "viewed": "https://api.socialverseapp.com/posts/view?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if"
    "liked": "https://api.socialverseapp.com/posts/like?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if"
    "inspired": "https://api.socialverseapp.com/posts/inspire?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if"
    "rated": "https://api.socialverseapp.com/posts/rating?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if"
    "summary": "https://api.socialverseapp.com/posts/summary/get?page=1&page_size=1000"
    "users": "https://api.socialverseapp.com/users/get_all?page=1&page_size=1000"

The flic token can be found in config.py

```bash
python3 main.py
```

# To run the Web App

```bash
python3 app.py
```

This will start the server, and you can access the web app by opening your browser and navigating to:
http://127.0.0.1:5000/

###

Once the web app is running, you can interact with the system via the user interface to generate video recommendations. You can input your preferences (such as mood and category), and the system will display personalized video recommendations based on the hybrid recommendation algorithm.
Refer the project report for in depth detail.
