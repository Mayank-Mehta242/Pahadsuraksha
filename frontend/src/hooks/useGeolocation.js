import { useState } from "react";

/**
 * Wraps the browser Geolocation API. Purely client-side — no backend
 * dependency — but the resulting {lat, lng} is what gets sent to
 * predictionService / incidentService once those are wired up.
 */
export function useGeolocation() {
  const [position, setPosition] = useState(null);
  const [error, setError] = useState(null);
  const [locating, setLocating] = useState(false);

  function locate() {
    if (!navigator.geolocation) {
      setError("Geolocation is not supported on this device.");
      return;
    }
    setLocating(true);
    setError(null);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setPosition({ lat: pos.coords.latitude, lng: pos.coords.longitude });
        setLocating(false);
      },
      (err) => {
        setError(err.message || "Unable to fetch your location.");
        setLocating(false);
      },
      { enableHighAccuracy: true, timeout: 10000 }
    );
  }

  return { position, error, locating, locate };
}
