import { useState } from "react";
import AddressForm from "./AddressForm";
import MapView from "./MapView";

function DynamicRoute() {
  const [routeData, setRouteData] = useState([]);
  const [distance, setDistance] = useState(null);

  const handleDynamicSubmit = async ({ addresses, start }) => {
    const res = await fetch("http://localhost:8000/dynamic-route", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ addresses, start }),
    });
    const data = await res.json();
    setRouteData(data.route);
    setDistance(data.distance?.toFixed(2));
  };

  return (
    <div className="max-w-5xl mx-auto mt-8 space-y-4">
      <h2 className="text-2xl font-semibold text-green-800">Dynamic Shortest Path</h2>
      <AddressForm onSubmit={handleDynamicSubmit} />
      {distance && <p className="text-green-700">Total Distance: {distance} miles</p>}
      {routeData.length > 0 && <MapView routeData={routeData} />}
    </div>
  );
}

export default DynamicRoute;
