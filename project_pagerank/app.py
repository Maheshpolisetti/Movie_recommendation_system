from flask import Flask, render_template, jsonify, request
import pandas as pd
import networkx as nx

app = Flask(__name__, template_folder="templates")

# Sample movies data
edges_df = pd.read_csv(r"project_pagerank\movie_edges.csv",usecols=["source","target","weight"])
movies=pd.read_csv(r"project_pagerank\datasets\mymoviedb.csv",usecols=["Title","Overview","Original_Language","Genre","Poster_Url"],nrows=1105)
pagerank_scores=pd.read_csv(r"project_pagerank\pagerank_scores.csv",usecols=["movie","pagerank"])

# movies["Overview"] = movies["Overview"].apply(lambda x: truncate_text(x, 20))

pagerank_scores.sort_values(by="pagerank", ascending=False, inplace=True)

G = nx.Graph()
for _, row in edges_df.iterrows():
    G.add_edge(row["source"], row["target"], weight=row["weight"])

def truncate_text(text, word_limit=20):
    """Truncate text to a given number of words."""
    words = text.split()  
    if len(words) > word_limit:
        return " ".join(words[:word_limit]) + "..."  # Add '...' if truncated
    return text

movies["Overview"] = movies["Overview"].apply(lambda x: truncate_text(x, 10))

def get_top_movies(n=10, exclude=[]):
    """Fetch top N movies from PageRank scores, excluding watched movies."""
    top_movies = pagerank_scores[~pagerank_scores["movie"].isin(exclude)].head(n)["movie"].tolist()
    
    duplicate=set(top_movies)
    duplicate=list(duplicate)

    filtered_movies = movies[movies["Title"].isin(duplicate)][
        ["Title", "Overview", "Original_Language", "Genre", "Poster_Url"]
    ]
    filtered_movies=filtered_movies.head(n)
    
    return filtered_movies.to_dict(orient="records")


def get_connected_movies(movie, exclude=[]):
    """Get movies connected to a given movie with highest weight."""
    if movie not in G:
        return []
    
    connections = [(neighbor, G[movie][neighbor]["weight"]) for neighbor in G.neighbors(movie)]
    connections = sorted(connections, key=lambda x: x[1], reverse=True)
    
    recommended_movies = [m for m, _ in connections if m not in exclude]
    
    return recommended_movies[:3]


@app.route("/")
def home():
    return render_template("index.html")

@app.route('/get_movies', methods=['GET'])
def get_movies():
    movies_df=get_top_movies()
    return jsonify(movies_df)

@app.route("/get_genres", methods=["GET"])
def get_genres():
    """Fetch all unique genres from the dataset"""
    all_genres = set()
    
    for genres in movies["Genre"].dropna():  
        genre_list = genres.split(", ")
        all_genres.update(genre_list)  
    
    return jsonify(sorted(all_genres))

@app.route("/get_movies_by_genre", methods=["GET"])
def get_movies_by_genre():
    genre = request.args.get("genre", "").lower()
    watched_movies = request.args.getlist("watched")

    if genre == "all":
        return jsonify(get_top_movies(n=10, exclude=watched_movies))

    genre_movies = movies[movies["Genre"].str.lower().str.contains(genre)]
    genre_pagerank = pagerank_scores[pagerank_scores["movie"].isin(genre_movies["Title"])]
    genre_pagerank_sorted = genre_pagerank.sort_values(by="pagerank", ascending=False)

    # top_genre_movies = genre_pagerank_sorted[~genre_pagerank_sorted["movie"].isin(watched_movies)].head(7)["movie"].tolist()

    history_recommendations = set()
    for movie in watched_movies:
        if movie in G:
            history_recommendations.update(get_connected_movies(movie, exclude=watched_movies))

    history_recommendations = list(history_recommendations)[:3]

    n1=10-len(history_recommendations)
    
    top_genre_movies = genre_pagerank_sorted[~genre_pagerank_sorted["movie"].isin(watched_movies)].head(n1)["movie"].tolist()
    recommended_movies = movies[movies["Title"].isin(history_recommendations + top_genre_movies)][
        ["Title", "Overview", "Original_Language", "Genre", "Poster_Url"]
    ].to_dict(orient="records")
    recommended_movies=recommended_movies[:10]

    return jsonify(recommended_movies)

@app.route("/recommend_movies", methods=["POST"])
def recommend_movies():
    watched_movies = request.json.get("watched", [])
    recommended = set()

    for movie in watched_movies:
        if movie in G:
            recommended.update(get_connected_movies(movie, exclude=watched_movies))

    recommended = list(recommended)[:3]
    n1=10-len(recommended)  # Get at most 3 movies from history-based recommendations
    remaining_movies = get_top_movies(n=n1, exclude=watched_movies + recommended)  # Get remaining movies from PageRank

    recommended_movies = movies[movies["Title"].isin(recommended)][
        ["Title", "Overview", "Original_Language", "Genre", "Poster_Url"]
    ]

    # total_movies=recommended_movies + remaining_movies
    # total_movies=total_movies.sort(lambda x: )
    remaining_movies_df = pd.DataFrame(remaining_movies)  

    total_movies = pd.concat([recommended_movies, remaining_movies_df])
    total_movies = total_movies.merge(pagerank_scores, left_on="Title", right_on="movie", how="left")

    total_movies = total_movies.sort_values(by="pagerank", ascending=False)

    # Convert back to JSON-friendly format
    total_movies = total_movies.drop(columns=["pagerank", "movie"]).to_dict(orient="records")


    return jsonify(total_movies)



@app.route("/search_movies", methods=["GET"])
def search_movies():
    search_query = request.args.get("title", "").strip().lower()

    matched_title = next((title for title in G.nodes if title.lower().strip() == search_query), None)

    if not matched_title:
        print(f"Movie '{search_query}' not found in graph.")
        return jsonify([]) 
    
    recommends = {matched_title}
    recommends.update(get_connected_movies(matched_title))

    recommended_movies = movies[movies["Title"].isin(recommends)][
        ["Title", "Overview", "Original_Language", "Genre", "Poster_Url"]
    ].to_dict(orient="records")

    return jsonify(recommended_movies)

if __name__ == '__main__':
    app.run(debug=True)

