import { useState } from "react";
import MapView from "../components/MapView";

function StaticRoute({ handleShowStatic, routeData, distance }) {
  const [loaded, setLoaded] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchAndShow = async () => {
    setLoading(true);
    setError(null);
    try {
      await handleShowStatic();
      setLoaded(true);
    } catch (err) {
      setError("Failed to fetch static route. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h2 className="text-3xl font-bold text-blue-900 mb-4">
        📌 Static Route — All Known Points from UCI ISEB
      </h2>
      <p className="mb-6 text-gray-700 text-lg">
        This tool computes the shortest round trip starting and ending at UCI ISEB, visiting all known addresses in the dataset. Great for pre-defined delivery or inspection routes.
      </p>

      <button
        onClick={fetchAndShow}
        className="mb-6 px-6 py-3 bg-blue-600 text-white text-lg rounded-xl shadow hover:bg-blue-700 transition"
      >
        🚀 Generate Static Route
      </button>

      {loading && (
        <div className="text-center text-blue-700 text-lg">Loading route...</div>
      )}

      {error && (
        <div className="text-center text-red-600 font-medium mt-4">{error}</div>
      )}

      {routeData.length > 0 && loaded && (
        <div className="space-y-4">
          <div className="h-[70vh] rounded-xl overflow-hidden shadow">
            <MapView routeData={routeData} />
          </div>
          <div className="text-center text-sm text-gray-400">
            🔍 Zoom in on the map to view visiting order.
          </div>
          <div className="text-gray-800 text-lg font-medium">
            🧭 Total Distance: <span className="font-bold">{distance.toFixed(2)} miles</span>
          </div>
        </div>
      )}

      {!loaded && !loading && (
        <div className="text-gray-500 mt-10 text-center">
          <p>Click the button above to visualize the optimal static path.</p>
        </div>
      )}
    </div>
  );
}

export default StaticRoute;