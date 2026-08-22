import { useEffect } from "react";
import { MapContainer, TileLayer, CircleMarker, Popup, useMap, useMapEvents } from "react-leaflet";
import { TEHRI_GARHWAL_CENTER, DEFAULT_ZOOM } from "../utils/constants.js";
import { normalizeRiskKey, RISK_STYLES } from "../utils/riskUtils.js";

const RISK_HEX = {
  low: "#22A567",
  medium: "#E0B324",
  high: "#E07A24",
  extreme: "#C7362B",
};

function ClickCapture({ onMapClick }) {
  useMapEvents({
    click(e) {
      onMapClick?.(e.latlng);
    },
  });
  return null;
}

function LocationMarker({ position }) {
  const map = useMap();

  useEffect(() => {
    if (position) map.flyTo([position.lat, position.lng], Math.max(map.getZoom(), 12), { duration: 1 });
  }, [map, position]);

  if (!position) return null;
  return (
    <CircleMarker
      center={[position.lat, position.lng]}
      radius={8}
      pathOptions={{ color: "#14532d", fillColor: "#4ade80", fillOpacity: 0.9, weight: 3 }}
    >
      <Popup>You are here</Popup>
    </CircleMarker>
  );
}

export default function MapView({ districts = [], onSelectDistrict, onMapClick, userPosition, height = "480px" }) {
  return (
    <div style={{ height }} className="rounded overflow-hidden border border-slate-700">
      <MapContainer
        center={[TEHRI_GARHWAL_CENTER.lat, TEHRI_GARHWAL_CENTER.lng]}
        zoom={DEFAULT_ZOOM}
        style={{ height: "100%", width: "100%" }}
        scrollWheelZoom
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <ClickCapture onMapClick={onMapClick} />
        <LocationMarker position={userPosition} />
        {districts.map((d) => (
          <CircleMarker
            key={d.id}
            center={[d.lat, d.lng]}
            radius={10}
            pathOptions={{
              color: RISK_HEX[normalizeRiskKey(d.risk)],
              fillColor: RISK_HEX[normalizeRiskKey(d.risk)],
              fillOpacity: 0.55,
              weight: 2,
            }}
            eventHandlers={{
              click: () => onSelectDistrict?.(d),
            }}
          >
            <Popup>
              <div className="text-sm">
                <p className="font-semibold">{d.name}</p>
                <p>Risk: {RISK_STYLES[normalizeRiskKey(d.risk)].label}</p>
                <p>Incidents (YTD): {d.incidents}</p>
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
}
