import React, { useState } from 'react';
import axios from '../axios';

export default function TrainModel({ datasetId }) {
  const [target, setTarget] = useState('');
  const [modelName, setModelName] = useState('');

  const train = async () => {
    try {
      const res = await axios.post(`train/${datasetId}/`, {
        target,
        model_name: modelName
      });
      alert(`Model trained and saved! Version: ${res.data.version}`);
    } catch (err) {
      console.error(err);
      alert('Training failed');
    }
  };

  return (
    <div>
      <h3>Train Model</h3>
      <input placeholder="Target column" onChange={e => setTarget(e.target.value)} />
      <input placeholder="Model name" onChange={e => setModelName(e.target.value)} />
      <button onClick={train}>Train & Save</button>
    </div>
  );
}