import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useState } from "react";
import Navbar from "./components/Navbar";
import Home from "./components/Home";
import StaticRoute from "./components/StaticRoute";
import DynamicRoute from "./components/DynamicRoute";
import Team from "./components/Team";

function App() {
  const [routeData, setRouteData] = useState([]);
  const [distance, setDistance] = useState(0);

  const handleShowStatic = async () => {
    try {
      const res = await fetch("http://localhost:8000/static-route");
      const data = await res.json();
      setRouteData(data.route || data); // support both formats
      setDistance(data.distance || 0);
    } catch (err) {
      console.error("Failed to fetch static route:", err);
    }
  };

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-white to-blue-100 font-sans">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route
            path="/static"
            element={
              <StaticRoute
                handleShowStatic={handleShowStatic}
                routeData={routeData}
                distance={distance}
              />
            }
          />
          <Route path="/dynamic" element={<DynamicRoute />} />
          <Route path="/team" element={<Team />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;





// import { useState } from 'react';
// import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
// import MapView from './components/MapView';
// import AddressForm from './components/AddressForm';

// function App() {
//   const [routeType, setRouteType] = useState(null);
//   const [routeData, setRouteData] = useState([]);
//   const [distance, setDistance] = useState(0);

//   const handleShowStatic = async () => {
//     try {
//       const res = await fetch("http://localhost:8000/static-route");
//       const data = await res.json();
//       setRouteType("static");
//       setRouteData(data.route || data); // support older return format
//       setDistance(data.distance || 0);
//     } catch (err) {
//       console.error("Failed to fetch static route:", err);
//     }
//   };

//   const handleDynamicSubmit = async ({ addresses, start }) => {
//     try {
//       const res = await fetch("http://localhost:8000/dynamic-route", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ addresses, start }),
//       });
//       const data = await res.json();
//       setRouteType("dynamic");
//       setRouteData(data.route || data);
//       setDistance(data.distance || 0);
//     } catch (err) {
//       console.error("Failed to fetch dynamic route:", err);
//     }
//   };

//   return (
//     <Router>
//       <div className="min-h-screen bg-gradient-to-br from-white to-blue-100 font-sans">
//         <nav className="bg-white shadow sticky top-0 z-50">
//           <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
//             <div className="text-xl font-bold text-blue-800">UCI TSP Mapper</div>
//             <div className="flex gap-6 text-gray-600 font-medium">
//               <Link to="/">Home</Link>
//               <Link to="/static">Static Route</Link>
//               <Link to="/dynamic">Dynamic Route</Link>
//               <Link to="/team">Team</Link>
//             </div>
//           </div>
//         </nav>

//         <Routes>
//           <Route path="/" element={
//             <div className="max-w-4xl mx-auto p-6 text-gray-800">
//               <h1 className="text-4xl font-bold mb-4">Welcome to the UCI TSP Route Visualizer</h1>
//               <p className="mb-4">This platform was built by UCI students as part of the "Soar Into Data" Datathon challenge. It helps calculate the most efficient path to visit multiple addresses around UCI.</p>
//               <p className="mb-4">There are two tools available:</p>
//               <ul className="list-disc list-inside mb-6">
//                 <li><strong>Static Shortest Path Calculator:</strong> Calculates the shortest round trip starting from UCI ISEB to visit all known points.</li>
//                 <li><strong>Dynamic Shortest Path Calculator:</strong> You select points and a starting address, and it calculates the best route.</li>
//               </ul>
//               <div className="flex gap-4">
//                 <Link to="/static" className="bg-blue-500 text-white px-6 py-3 rounded-xl hover:bg-blue-600 transition">Static Shortest Path Calculator</Link>
//                 <Link to="/dynamic" className="bg-green-500 text-white px-6 py-3 rounded-xl hover:bg-green-600 transition">Dynamic Shortest Path Calculator</Link>
//               </div>
//             </div>
//           } />

//           <Route path="/static" element={
//             <div className="max-w-5xl mx-auto p-6">
//               <h2 className="text-2xl font-semibold mb-4">Static Route (All Points from UCI ISEB)</h2>
//               <button onClick={handleShowStatic} className="mb-4 px-5 py-2 bg-blue-600 text-white rounded-lg">Generate Static Route</button>
//               {routeData.length > 0 && (
//                 <>
//                   <div className="h-[70vh] rounded-xl overflow-hidden">
//                     <MapView routeData={routeData} />
//                   </div>
//                   <p className="mt-4 text-lg font-medium text-gray-700">Total Distance: {distance.toFixed(2)} miles</p>
//                 </>
//               )}
//             </div>
//           } />

//           <Route path="/dynamic" element={
//             <div className="max-w-5xl mx-auto p-6">
//               <h2 className="text-2xl font-semibold mb-4">Dynamic Route (Choose Addresses)</h2>
//               <AddressForm onSubmit={handleDynamicSubmit} />
//               {routeData.length > 0 && (
//                 <>
//                   <div className="h-[70vh] rounded-xl overflow-hidden mt-4">
//                     <MapView routeData={routeData} />
//                   </div>
//                   <p className="mt-4 text-lg font-medium text-gray-700">Total Distance: {distance.toFixed(2)} miles</p>
//                 </>
//               )}
//             </div>
//           } />

//           <Route path="/team" element={
//             <div className="max-w-6xl mx-auto p-6">
//               <h2 className="text-3xl font-bold mb-6">Meet the Team</h2>
//               <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
//                 {TEAM.map((member, idx) => (
//                   <div key={idx} className="bg-white p-4 shadow rounded-xl text-center">
//                     <img src={member.image} alt={member.name} className="w-24 h-24 rounded-full mx-auto mb-4" />
//                     <h3 className="text-xl font-semibold text-blue-800">{member.name}</h3>
//                     <p className="text-gray-600 text-sm">{member.role}</p>
//                     <div className="mt-2">
//                       <a href={member.linkedin} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">LinkedIn</a>
//                     </div>
//                   </div>
//                 ))}
//               </div>
//             </div>
//           } />
//         </Routes>
//       </div>
//     </Router>
//   );
// }

// // Placeholder team global variable (replace with real data later)
// const TEAM = [
//   {
//     name: "Alice",
//     role: "Frontend Dev",
//     linkedin: "https://linkedin.com/in/alice",
//     image: "https://via.placeholder.com/100"
//   },
//   {
//     name: "Bob",
//     role: "Backend Dev",
//     linkedin: "https://linkedin.com/in/bob",
//     image: "https://via.placeholder.com/100"
//   },
//   {
//     name: "Charlie",
//     role: "ML Engineer",
//     linkedin: "https://linkedin.com/in/charlie",
//     image: "https://via.placeholder.com/100"
//   }
// ];

// export default App;
