import React, { useRef, useEffect, useState } from "react";

function App() {
  const videoRef = useRef(null);
  const [result, setResult] = useState(null);
  const [isStreaming, setIsStreaming] = useState(false);

  // Initialise la caméra
  useEffect(() => {
    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error("Erreur lors de l'accès à la caméra :", err);
      }
    };

    startCamera();
  }, []);

  // Capture une image et envoie au backend
  const handleCaptureAndSend = async () => {
    if (!videoRef.current) return;
  
    // Crée un canvas pour capturer une image de la vidéo
    const canvas = document.createElement("canvas");
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
  
    // Convertit l'image en Blob (format image)
    canvas.toBlob(async (blob) => {
      if (!blob) return;
  
      const formData = new FormData();
      formData.append("image", blob, "snapshot.jpg");
  
      try {
        const response = await fetch("http://localhost:5000/upload", {
          method: "POST",
          body: formData,
        });
        const data = await response.json();
        setResult(data);
      } catch (err) {
        console.error("Erreur lors de l'envoi :", err);
      }
    }, "image/jpeg");
  };
  

  // Envoie une image toutes les deux secondes
  useEffect(() => {
    let interval;
    if (isStreaming) {
      interval = setInterval(captureAndSend, 10000);
    }
    return () => clearInterval(interval); // Nettoie l'intervalle si le composant est démonté
  }, [isStreaming]);

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Caméra et traitement d'image</h1>
      <video
        ref={videoRef}
        autoPlay
        style={{
          width: "80%",
          maxWidth: "600px",
          borderRadius: "8px",
          boxShadow: "0 4px 8px rgba(0,0,0,0.2)",
        }}
      ></video>
      <div style={{ margin: "20px" }}>
        <button onClick={handleCaptureAndSend}>
          Envoyer
        </button>
      </div>
      {result && (
        <pre
          style={{
            textAlign: "left",
            backgroundColor: "#f0f0f0",
            padding: "10px",
            borderRadius: "5px",
            maxWidth: "600px",
            margin: "0 auto",
          }}
        >
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  );
}

export default App;
