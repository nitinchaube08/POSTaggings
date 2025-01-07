
import { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {

  const [message, setMessage]= useState('')

  useEffect(()=>{
    axios.get('http://127.0.0.1:5000/')
      .then(response  => setMessage(response.data.message))
      .catch(error => console.error("Error fetching data: ",error));
  }, [])

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Grammar checing using POS tagging.</h1>
      <p> Frontend is ok!</p>
      <p>{message}</p>
    </div>
  );
}

export default App;
