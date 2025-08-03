"use client";

import { useState, useRef } from "react";

export default function VoiceRec() {
  const [btnStatus, setBtnStatus] = useState("");
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const startRecord = async () => {
    setBtnStatus("listening");
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        chunksRef.current.push(e.data);
      };

      mediaRecorder.onstop = async () => {
        setBtnStatus("loading");
        const blob = new Blob(chunksRef.current, { type: "audio/wav" });

        try {
          const response = await fetch(
            "http://localhost:8000/api/v1/voice/transcribe",
            {
              method: "POST",
              body: createFormData(blob),
              credentials: "include",
            }
          );

          const data = await response.json();
          speakText(data.text || "");
        } catch (error) {
          console.error("Error:", error);
        } finally {
          setBtnStatus("");
          cleanup();
        }
      };

      mediaRecorder.start();
    } catch (error) {
      console.error("Error accessing microphone:", error);
      setBtnStatus("");
    }
  };

  const stopRecord = () => {
    if (
      mediaRecorderRef.current &&
      mediaRecorderRef.current.state === "recording"
    ) {
      mediaRecorderRef.current.stop();
      cleanup();
    }
  };

  const cleanup = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stream
        .getTracks()
        .forEach((track) => track.stop());
      mediaRecorderRef.current = null;
    }
    chunksRef.current = [];
  };

  const createFormData = (blob: Blob) => {
    const formData = new FormData();
    formData.append("audio", blob, "recording.wav");
    return formData;
  };

  const speakText = (text: string) => {
    if ("speechSynthesis" in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      window.speechSynthesis.speak(utterance);
    }
  };

  return (
    <button
      onMouseDown={startRecord}
      onMouseUp={stopRecord}
      onMouseLeave={stopRecord}
      onTouchStart={startRecord}
      onTouchEnd={stopRecord}
      style={{
        borderRadius: "50%",
        width: "100px",
        height: "100px",
        position: "relative",
        background: "transparent",
      }}
      className="border-0"
    >
      {btnStatus === "listening" && (
        <div className="spinner-grow text-warning position-absolute top-0 start-0 w-100 h-100" />
      )}
      {btnStatus === "loading" && (
        <>
          <div className="spinner-border text-light position-absolute top-0 start-0 w-100 h-100 display-5" />
        </>
      )}
      {!btnStatus && (
        <div className="position-absolute top-0 start-0 w-100 h-100 bg-light rounded-circle" />
      )}
    </button>
  );
}
