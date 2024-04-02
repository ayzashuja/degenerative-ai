// import logo from './logo.svg';
// import './App.css';
import Home from './components/Home.js';
import Login from './components/Login.js';
import Signup from './components/Signup.js';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useState } from 'react';
import React, { Component } from "react";


function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/home" element={<Home />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
