import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="text-center px-6 py-12 max-w-3xl mx-auto text-gray-800">
      <h1 className="text-5xl font-bold mb-6 flex justify-center items-center gap-2">
        <span role="img" aria-label="satellite">🛰️</span> Soar Into Data
      </h1>

      <p className="text-gray-700 text-lg mb-4">
        This project visualizes optimal routes for delivery or exploration using the
        <strong> Travelling Salesman Problem</strong>. It was created as part of the Datathon at UCI.
      </p>

      <p className="text-gray-600 text-md mb-8">
        Built by a team of 3 students from UC Irvine, this app provides two main functionalities:
      </p>

      <div className="flex flex-col md:flex-row gap-6 justify-center mb-8">
        <Link
          to="/static"
          className="bg-blue-600 text-white py-3 px-6 rounded-xl shadow-md hover:bg-blue-700 transition"
        >
          📌 Static Shortest Route Calculator
        </Link>
        <Link
          to="/dynamic"
          className="bg-green-600 text-white py-3 px-6 rounded-xl shadow-md hover:bg-green-700 transition"
        >
          🧭 Dynamic Shortest Route Calculator
        </Link>
      </div>

      <div className="text-sm text-gray-500 italic leading-relaxed">
        <p>
          <em>
            This year’s theme, <strong>Soar into Data</strong>, serves as a beacon guiding us through the
            world of unexplored data. Let’s unravel the mysteries, decode the patterns, and reach
            new horizons together.
          </em>
        </p>
      </div>
    </div>
  );
}

export default Home;
