import React, { useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

export default function Predict() {
  const { modelId } = useParams();
  const [inputData, setInputData] = useState({});
  const [prediction, setPrediction] = useState(null);

  const handleChange = (e) => {
    setInputData({ ...inputData, [e.target.name]: e.target.value });
  };

  const predict = () => {
    axios.post(`http://localhost:8000/api/predict/${modelId}/`, { input: inputData }, {
      headers: { Authorization: `Token ${localStorage.getItem('token')}` }
    }).then(res => {
      setPrediction(res.data.prediction);
    });
  };

  return (
    <div>
      <h2>Predict</h2>
      <p>Enter input features below (match your dataset):</p>
      <textarea
        rows="6"
        cols="50"
        placeholder='e.g. {"feature1": 3.5, "feature2": 2}'
        onChange={(e) => setInputData(JSON.parse(e.target.value))}
      />
      <br />
      <button onClick={predict}>Predict</button>
      {prediction !== null && (
        <h4>Prediction: {prediction.toString()}</h4>
      )}
    </div>
  );
}
