import os
from flask import Flask, request, jsonify, redirect, session
from flask_session import Session
import requests
from rymscraper import scrape_rym_top_songs
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management
app.config['SESSION_TYPE'] = 'filesystem'  # Store session data in the filesystem
Session(app) # Initialize the session

CORS(app, supports_credentials=True, origins=['http://localhost:3000'])

SPOTIFY_CLIENT_ID = '44a84bad90034dcb8f9058830b78305d'
SPOTIFY_CLIENT_SECRET = '355393d91f0b48929b2c21ebf9bf414b'
SPOTIFY_REDIRECT_URI = 'http://localhost:5000/callback'
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_URL = 'https://api.spotify.com/v1'

def get_spotify_auth_url():
    scope = 'playlist-modify-public playlist-modify-private user-read-private' # Permissions required for creating playlists
    return (f'{SPOTIFY_AUTH_URL}?response_type=code&'
            f'client_id={SPOTIFY_CLIENT_ID}&'
            f'scope={scope}&'
            f'redirect_uri={SPOTIFY_REDIRECT_URI}')

@app.route('/test-cors')
def test_cors():
    return 'CORS is working!'

@app.route('/')
def index():
    return redirect(get_spotify_auth_url())

# Callback route for Spotify authorization
@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return 'No code received', 400

    response = requests.post(SPOTIFY_TOKEN_URL, {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET
    })

    data = response.json()
    access_token = data.get('access_token')
    session['access_token'] = access_token

    print('Access token:', session['access_token'])

    return redirect('http://localhost:3000/playlist_form')

@app.route('/generate_playlist', methods=['POST'])
def generate_playlist():
    access_token = session.get('access_token')
    print('Access token:', access_token)
    if not access_token:
        return redirect('/')

    data = request.form
    year = data.get('year', 'all-time')
    genre = data.get('genre', None)
    artist = data.get('artist', None)

    songs = scrape_rym_top_songs(year, genre, artist)
    print('songs: ', songs)

    # Get user ID
    user_id_response = requests.get(f'{SPOTIFY_API_URL}/me', headers={
        'Authorization': f'Bearer {access_token}'
    })
    user_id = user_id_response.json().get('id')
    print(user_id_response.json())

    # playlist name should be 'Top {genre} Songs of {year} by {artist}' where artist and genre are optional
    playlist_name = f'Top rym'
    if genre:
        playlist_name += f' {genre}'
    playlist_name += f' songs of {year}'
    if artist:
        playlist_name += f' by {artist}'

    playlist_response = requests.post(f'{SPOTIFY_API_URL}/users/{user_id}/playlists', json={
        'name': playlist_name,
        'description': 'A playlist of top songs from Rate Your Music',
        'public': True
    }, headers={
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    })

    print(playlist_response.json())

    playlist_id = playlist_response.json().get('id')

    # Add tracks to the playlist
    track_uris = [f'spotify:track:{song['track_id']}' for song in songs]
    requests.post(f'{SPOTIFY_API_URL}/playlists/{playlist_id}/tracks', json={
        'uris': track_uris
    }, headers= {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    })

    # Prepare response with CORS headers
    response = jsonify({
        'playlist_id': playlist_id,
        'playlist_name': playlist_name
    })
    
    return response

if __name__ == '__main__':
    app.run(debug=True)