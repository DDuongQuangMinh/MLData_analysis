import React, { useEffect, useState } from 'react';
import axios from '../axios';

export default function ModelManager() {
  const [models, setModels] = useState([]);
  const [newName, setNewName] = useState('');

  const loadModels = async () => {
    const res = await axios.get('models/');
    setModels(res.data);
  };

  const deleteModel = async (id) => {
    await axios.delete(`models/delete/${id}/`);
    loadModels();
  };

  const renameModel = async (id) => {
    await axios.post(`models/rename/${id}/`, { new_name: newName });
    loadModels();
  };

  useEffect(() => {
    loadModels();
  }, []);

  return (
    <div>
      <h3>Your Models</h3>
      <ul>
        {models.map(model => (
          <li key={model.id}>
            {model.name} (v{model.version})
            <button onClick={() => deleteModel(model.id)}>Delete</button>
            <input placeholder="Rename to" onChange={e => setNewName(e.target.value)} />
            <button onClick={() => renameModel(model.id)}>Rename</button>
          </li>
        ))}
      </ul>
    </div>
  );
}