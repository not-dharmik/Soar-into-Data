import {
    MapContainer,
    TileLayer,
    CircleMarker,
    Polyline,
    Popup,
  } from 'react-leaflet';
  import 'leaflet/dist/leaflet.css';
  
  function MapView({ routeData }) {
    const defaultCenter = [33.6405, -117.8443]; // UCI coordinates
    const path = routeData.map((p) => [p.lat, p.lon]);
  
    return (
      <MapContainer center={defaultCenter} zoom={16} className="h-full w-full rounded-xl">
        <TileLayer
          attribution="&copy; OpenStreetMap contributors"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {routeData.map((point, idx) => (
          <CircleMarker
            key={idx}
            center={[point.lat, point.lon]}
            radius={4}
            pathOptions={{
              color: '#1d4ed8',        // stroke
              fillColor: '#1d4ed8',    // fill
              fillOpacity: 1,
            }}
          >
            <Popup>{point.address}</Popup>
          </CircleMarker>
        ))}
        <Polyline positions={path} color="blue" />
      </MapContainer>
    );
  }
  
  export default MapView;
  