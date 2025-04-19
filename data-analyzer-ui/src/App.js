import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './Login';
import Upload from './Upload';
import EDA from './EDA';
import TrainModel from './TrainModel';
import Predict from './Predict';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/eda/:datasetId" element={<EDA />} />
        <Route path="/train/:datasetId" element={<TrainModel />} />
        <Route path="/predict/:modelId" element={<Predict />} />
      </Routes>
    </Router>
  );
}

export default App;