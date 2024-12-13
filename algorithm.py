from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from moodextractor import extract_moods
from collections import Counter
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
df_summary['category_name'] = df_summary['category'].apply(lambda x: x.get('name') if isinstance(x, dict) else None)
columns = ['id', 'title', 'video_link', 'category_name', 'username', 'upvote_count', 'view_count', 'rating_count', 'moods']
df_recommend = df_summary[columns]  
df_recommend = df_recommend.copy()  # Create a deep copy
df_recommend['features'] = df_recommend['moods'].apply(
    lambda moods: " ".join(moods) if isinstance(moods, list) else ""
) + " " + df_recommend['category_name'].astype(str)


interaction_matrix = df_recommend.pivot(index='username', columns='id', values='upvote_count').fillna(0)

# Matrix Factorization
svd = TruncatedSVD(n_components=50)
latent_matrix = svd.fit_transform(interaction_matrix)

vectorizer = TfidfVectorizer()
feature_matrix = vectorizer.fit_transform(df_recommend['features'])

# function for calculating collaborative filtering scores
def get_cf_scores(username, top_n=10):
    user_index = interaction_matrix.index.get_loc(username)
    user_latent = latent_matrix[user_index]
    scores = cosine_similarity([user_latent], latent_matrix)[0]
    top_indices = scores.argsort()[-top_n:][::-1]
    return interaction_matrix.iloc[top_indices].index.tolist()

# function for calculating content based filtering
def get_cbf_scores(user_mood, user_category, top_n=10):
    user_feature = f"{user_mood} {user_category}"
    user_vector = vectorizer.transform([user_feature])
    scores = cosine_similarity(user_vector, feature_matrix).flatten()
    top_indices = scores.argsort()[-top_n:][::-1]
    return df_recommend.iloc[top_indices]

# hybrid function which incorporates properties of both collaborative and content based filtering
def get_hybrid_recommendations(username, mood, category, top_n=10, alpha=0.7):
    """
    Hybrid recommendation combining collaborative filtering (CF) and content-based filtering (CBF).
    """
    # CF Recommendations
    cf_scores = get_cf_scores(username, top_n)
    # print(cf_scores)
    cf_recommendations = df_recommend[df_recommend['username'].isin(cf_scores)].copy()
    cf_recommendations['cf_score'] = range(len(cf_recommendations), 0, -1)
    cf_recommendations = cf_recommendations.sort_values(by='cf_score', ascending=False).head(10)
    # print(cf_recommendations)
    
    # CBF Recommendations
    cbf_recommendations = get_cbf_scores(mood, category, top_n)
    cbf_recommendations['cbf_score'] = range(len(cbf_recommendations), 0, -1)
    # print(cbf_recommendations)
    
    # Merge CF and CBF Recommendations
    cf_recommendations = cf_recommendations.drop(columns=['cf_score'])
    cbf_recommendations = cbf_recommendations.drop(columns=['cbf_score'])

    # Merge the dataframes on 'id' without suffixes
    hybrid_df = pd.concat([cf_recommendations, cbf_recommendations], axis=0)

    # Reset the index after concatenation (optional)
    hybrid_df.reset_index(drop=True, inplace=True)
    hybrid_df['hybrid_score'] = 0.5 * hybrid_df['upvote_count'] + 0.3 * hybrid_df['view_count'] + 0.2 * hybrid_df['rating_count']

    top_10_recommendations = hybrid_df.sort_values(by='hybrid_score', ascending=False).head(10)
    return top_10_recommendations 