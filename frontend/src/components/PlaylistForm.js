// src/components/PlaylistForm.js
import React, { useState } from 'react';
import axios from 'axios';

const PlaylistForm = () => {
    const [year, setYear] = useState('');
    const [genre, setGenre] = useState('');
    const [artist, setArtist] = useState('');
    const [playlist, setPlaylist] = useState(null);
    const [error, setError] = useState(null);

    const handleSubmit = async (event) => {
        event.preventDefault();
        console.log(artist)

        try {
            const response = await axios.post('http://localhost:5000/generate_playlist', {
                year,
                genre,
                artist
            }, {
                withCredentials: true
            }, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            setPlaylist(response.data);
            setError(null);
        } catch (err) {
            setError('An error occurred while generating the playlist.');
            setPlaylist(null);
        }
    };

    return (
        <div>
            <h1>Generate Playlist</h1>
            <form onSubmit={handleSubmit}>
                <label htmlFor="year">Year:</label>
                <input
                    type="text"
                    id="year"
                    name="year"
                    value={year}
                    onChange={(e) => setYear(e.target.value)}
                />
                <br />
                <label htmlFor="genre">Genre:</label>
                <input
                    type="text"
                    id="genre"
                    name="genre"
                    value={genre}
                    onChange={(e) => setGenre(e.target.value)}
                />
                <br />
                <label htmlFor="artist">Artist:</label>
                <input
                    type="text"
                    id="artist"
                    name="artist"
                    value={artist}
                    onChange={(e) => setArtist(e.target.value)}
                />
                <br />
                <button type="submit">Generate Playlist</button>
            </form>
            {playlist && (
                <div>
                    <h2>Playlist Created</h2>
                    <p>Playlist Name: {playlist.playlist_name}</p>
                    <a href={`https://open.spotify.com/playlist/${playlist.playlist_id}`} target="_blank" rel="noopener noreferrer">
                        View Playlist
                    </a>
                </div>
            )}
            {error && <p>{error}</p>}
        </div>
    );
};

export default PlaylistForm;
