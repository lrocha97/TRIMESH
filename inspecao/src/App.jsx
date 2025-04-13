import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [dados, setDados] = useState(null);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await axios.post("http://localhost:8000/analisar/", formData);
    setDados(response.data);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Inspecionar Modelo 3D (.glb)</h1>
      <input type="file" accept=".glb" onChange={e => setFile(e.target.files[0])} />
      <button onClick={handleUpload} style={{ marginLeft: "1rem" }}>Enviar</button>

      {dados && (
        <div style={{ marginTop: "2rem" }}>
          <h2>Informações do Modelo</h2>
          <pre>{JSON.stringify(dados, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
