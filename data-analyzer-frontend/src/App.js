import React, { useState } from 'react';
import Register from './components/Register';
import Login from './components/Login';
import UploadAndEDA from './components/UploadAndEDA'; // from before
import TrainModel from './components/TrainModel';
import PredictSaved from './components/PredictSaved';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('access'));
  const [datasetId, setDatasetId] = useState(null); // should be set after uploading

  return (
    <div className="App">
      {!isLoggedIn ? (
        <>
          <Register />
          <Login setIsLoggedIn={setIsLoggedIn} />
        </>
      ) : (
        <>
          <UploadAndEDA setDatasetId={setDatasetId} />
          {datasetId && <TrainModel datasetId={datasetId} />}
          <PredictSaved />
        </>
      )}
    </div>
  );
}

export default App;