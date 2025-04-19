import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';

export default function TrainModel() {
  const { datasetId } = useParams();
  const [columns, setColumns] = useState([]);
  const [target, setTarget] = useState('');
  const [modelType, setModelType] = useState('decision_tree');
  const [accuracy, setAccuracy] = useState(null);
  const [models, setModels] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    axios.get(`http://localhost:8000/api/eda/${datasetId}/`, {
      headers: { Authorization: `Token ${localStorage.getItem('token')}` }
    }).then(res => setColumns(res.data.columns));

    axios.get(`http://localhost:8000/api/models/${datasetId}/`, {
      headers: { Authorization: `Token ${localStorage.getItem('token')}` }
    }).then(res => setModels(res.data));
  }, [datasetId]);

  const train = () => {
    axios.post(`http://localhost:8000/api/train/${datasetId}/`, { target, model_type: modelType }, {
      headers: { Authorization: `Token ${localStorage.getItem('token')}` }
    }).then(res => {
      setAccuracy(res.data.accuracy);
      setTimeout(() => navigate(`/predict/${res.data.model_id}`), 2000);
    });
  };

  return (
    <div>
      <h2>Train Model</h2>
      <label>Target Column:</label>
      <select onChange={e => setTarget(e.target.value)} value={target}>
        <option value="">-- Select --</option>
        {columns.map(col => (
          <option key={col} value={col}>{col}</option>
        ))}
      </select>
      <br />

      <label>Model Type:</label>
      <select onChange={e => setModelType(e.target.value)} value={modelType}>
        <option value="decision_tree">Decision Tree</option>
        <option value="random_forest">Random Forest</option>
        <option value="logistic_regression">Logistic Regression</option>
      </select>
      <br /><br />

      <button onClick={train} disabled={!target}>Train</button>
      {accuracy && <p>Trained! Accuracy: {accuracy}</p>}

      <h3>Previous Models:</h3>
      <ul>
        {models.map(m => (
          <li key={m.id}>
            {m.name} ({m.model_type}) — {new Date(m.created_at).toLocaleString()}
            <button onClick={() => navigate(`/predict/${m.id}`)}>Predict</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
