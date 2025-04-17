import { MapContainer, TileLayer, Marker, Polyline, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

function MapView({ routeData }) {
  const center = [33.6405, -117.8443]; // UCI coordinates

  const path = routeData.map(p => [p.lat, p.lon]);

  return (
    <MapContainer center={center} zoom={13} className="h-full w-full z-0">
      <TileLayer
        attribution='&copy; OpenStreetMap'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {routeData.map((point, idx) => (
        <Marker position={[point.lat, point.lon]} key={idx}>
          <Popup>{point.address}</Popup>
        </Marker>
      ))}
      <Polyline positions={path} color="blue" />
    </MapContainer>
  );
}

export default MapView;
