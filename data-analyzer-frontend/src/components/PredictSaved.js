import React, { useState } from 'react';
import axios from '../axios';

export default function PredictSaved() {
  const [modelName, setModelName] = useState('');
  const [version, setVersion] = useState('');
  const [input, setInput] = useState('[{"feature1": 1, "feature2": 2}]');
  const [result, setResult] = useState([]);

  const predict = async () => {
    try {
      const res = await axios.post('predict-saved/', {
        model_name: modelName,
        version: parseInt(version),
        input: JSON.parse(input)
      });
      setResult(res.data.predictions);
    } catch (err) {
      console.error(err);
      alert('Prediction failed');
    }
  };

  return (
    <div>
      <h3>Predict with Saved Model</h3>
      <input placeholder="Model Name" onChange={e => setModelName(e.target.value)} />
      <input placeholder="Version" onChange={e => setVersion(e.target.value)} />
      <textarea rows="5" value={input} onChange={e => setInput(e.target.value)} />
      <button onClick={predict}>Predict</button>

      {result.length > 0 && (
        <div>
          <h4>Predictions:</h4>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}