from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset and preprocess
movies_data = pd.read_csv('movies.csv')
movies_data['combined_features'] = (
    movies_data['genres'].fillna('') + ' ' +
    movies_data['keywords'].fillna('') + ' ' +
    movies_data['tagline'].fillna('') + ' ' +
    movies_data['cast'].fillna('') + ' ' +
    movies_data['director'].fillna('')
)
vectorizer = TfidfVectorizer()
feature_matrix = vectorizer.fit_transform(movies_data['combined_features'])

class CORSRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_POST(self):
        if self.path == '/recommend':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            movie_name = data.get('movie_name', '')
            try:
                idx = movies_data[movies_data['title'].str.contains(movie_name, case=False, na=False)].index[0]
                similarity_scores = cosine_similarity(feature_matrix[idx], feature_matrix).flatten()
                similar_movies = sorted(list(enumerate(similarity_scores)), key=lambda x: x[1], reverse=True)[1:6]
                # Remove score, only include movie titles
                recommendations = [{"title": movies_data.iloc[i]['title']} for i, score in similar_movies]
            except IndexError:
                recommendations = {"error": "Movie not found"}

            self._set_headers()
            self.wfile.write(json.dumps(recommendations).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=CORSRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print('Starting server on port 8000...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
