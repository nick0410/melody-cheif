from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# In-memory storage for users and their preferences
user_data = {}  # Dictionary to store user info
user_item_matrix = pd.DataFrame()  # Matrix for storing ratings (dummy preferences)

# 1. Add user function
def add_user(user_id, user_info):
    global user_data, user_item_matrix
    user_data[user_id] = user_info
    
    # Generate dummy ratings for user's preferences
    ratings = np.random.randint(1, 6, size=(1, len(user_info['preferences'])))
    temp_df = pd.DataFrame(ratings, columns=user_info['preferences'], index=[user_id])
    user_item_matrix = pd.concat([user_item_matrix, temp_df], axis=0)

# 2. Content-based recommendations function
def content_based_recommendations(user_data, instr=None):
    df = pd.DataFrame(user_data).T  # Convert user data into DataFrame for easy processing
    if instr:
        df = df[(df['instr1'].str.contains(instr, case=False, na=False)) |
                (df['instr2'].str.contains(instr, case=False, na=False))]
    return df

# 3. Collaborative filtering recommendations function
def collaborative_filtering_recommendations(user_item_matrix, user_id):
    if user_item_matrix.shape[0] < 2:
        return pd.DataFrame()  # No recommendations if there's only one user
    
    similarity_matrix = cosine_similarity(user_item_matrix)
    similarity_df = pd.DataFrame(similarity_matrix, index=user_item_matrix.index, columns=user_item_matrix.index)
    
    # Find similar users based on cosine similarity
    user_similarities = similarity_df[user_id]
    similar_users = user_similarities.sort_values(ascending=False).index[1:]
    
    recommended_musicians = pd.DataFrame()
    for similar_user in similar_users:
        similar_user_ratings = user_item_matrix.loc[similar_user]
        recommended_items = similar_user_ratings[similar_user_ratings >= 4]  # Recommend musicians rated 4 or above
        
        for musician in recommended_items.index:
            if musician not in recommended_musicians.index:
                recommended_musicians = pd.concat([recommended_musicians, pd.DataFrame({musician: [similar_user_ratings[musician]]})], axis=1)
    
    return recommended_musicians.T

# 4. Hybrid recommendations function (combines content-based and collaborative filtering)
def hybrid_recommendations(user_data, user_item_matrix, user_id, instr=None):
    content_recs = content_based_recommendations(user_data, instr)
    collab_recs = collaborative_filtering_recommendations(user_item_matrix, user_id)
    
    hybrid_recs = pd.concat([content_recs, collab_recs]).drop_duplicates().reset_index(drop=True)
    return hybrid_recs

# Route to add users
@app.route('/add_user', methods=['POST'])
def add_user_route():
    data = request.json
    user_id = data['user_id']
    user_info = data['user_info']
    add_user(user_id, user_info)
    return jsonify({"message": f"User {user_id} added successfully!"})

# Route to get recommendations
@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    data = request.json
    user_id = data['user_id']
    instr = data['instrument']
    hybrid_result = hybrid_recommendations(user_data, user_item_matrix, user_id, instr)
    return jsonify(hybrid_result.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
