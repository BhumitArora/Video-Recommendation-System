from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from moodextractor import extract_moods
from collections import Counter
from algorithm import get_cbf_scores, get_hybrid_recommendations, get_cf_scores
import pandas as pd
import json


# Load the data
file_path_summary = 'data_summary.json'
with open(file_path_summary, 'r') as file:
    json_data_summary = json.load(file)  

df_summary = pd.DataFrame(json_data_summary)

# Extract moods 
df_summary['moods'] = df_summary['post_summary'].apply(extract_moods)

# Flatten the 'moods' column, ensuring only hashable items (strings) are included
all_moods = []
for moods_list in df_summary['moods']:
    if isinstance(moods_list, list):
        for mood in moods_list:
            if isinstance(mood, str):
                all_moods.append(mood.lower())

# Use Counter to count the occurrences of each mood
mood_counts = Counter(all_moods)

# Convert the Counter to a DataFrame
mood_counts_df = pd.DataFrame(mood_counts.items(), columns=['Mood', 'Count']).sort_values(by='Count', ascending=False)

# Get moods with count greater than 100
moods_greater_than_100 = mood_counts_df[mood_counts_df['Count'] > 100]['Mood'].tolist()

# Modify the 'moods' column
df_summary['moods'] = df_summary['moods'].apply(
    lambda moods_list: [mood if mood in moods_greater_than_100 else 'other' for mood in moods_list]
    if isinstance(moods_list, list) else moods_list
)

# Exploding the 'moods' column
df_exploded = df_summary.explode('moods')

# Extract categories
df_summary['category_name'] = df_summary['category'].apply(lambda x: x.get('name') if isinstance(x, dict) else None)
columns = ['id', 'title', 'video_link', 'category_name', 'username', 'upvote_count', 'view_count', 'rating_count', 'moods']
df_recommend = df_summary[columns]  

interaction_matrix = df_recommend.pivot(index='username', columns='id', values='upvote_count').fillna(0)

df_recommend = df_recommend.copy()  # Create a deep copy
df_recommend['features'] = df_recommend['moods'].apply(
    lambda moods: " ".join(moods) if isinstance(moods, list) else ""
) + " " + df_recommend['category_name'].astype(str)

# Simulate user history
user_history = df_recommend.groupby('username')['category_name'].apply(list).reset_index()

# Initialize the FastAPI app
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class RecommendationRequest(BaseModel):
    username: str
    category_name: str
    mood: str

# Available moods
available_moods = [
    'determination', 'confidence', 'enthusiasm', 'contemplation', 'warmth', 
    'curiosity', 'excitement', 'urgency', 'hope', 'joy', 'passion', 
    'engagement', 'serenity', 'calmness', 'sincerity', 'other'
]

@app.get("/", response_class=HTMLResponse)
async def get_form():
    # Serve HTML page for input
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)

# Endpoint: Recommend posts for a user
@app.post("/recommendations/")
async def get_recommendations(request: RecommendationRequest):
    username = request.username
    mood = request.mood
    category_name = request.category_name
    
    if username in interaction_matrix.index:
        recommendations = get_hybrid_recommendations(username,category_name,mood)
    else:
        recommendations = get_cbf_scores(mood, category_name)
    
    recommended_videos = recommendations[['title', 'id', 'video_link']].to_dict(orient='records')
    return {"recommendations": recommended_videos}
