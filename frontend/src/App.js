// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/HomePage';
import PlaylistForm from './components/PlaylistForm';

function App() {
    return (
        <Router>
            <div className="App">
                <Routes>
                    <Route path="/playlist_form" element={<PlaylistForm />} />
                    <Route path="/" element={<HomePage />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
