import { Link, useLocation } from "react-router-dom";

const Navbar = () => {
  const location = useLocation();
  const active = (path) => location.pathname === path;

  return (
    <nav className="bg-white shadow sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
        <div className="text-xl font-bold text-blue-800">UCI Route Finder</div>
        <div className="flex gap-6 text-gray-600 font-medium">
          <Link to="/" className={active("/") ? "text-blue-600 font-semibold" : ""}>Home</Link>
          <Link to="/static" className={active("/static") ? "text-blue-600 font-semibold" : ""}>Static Route</Link>
          <Link to="/dynamic" className={active("/dynamic") ? "text-blue-600 font-semibold" : ""}>Dynamic Route</Link>
          <Link to="/team" className={active("/team") ? "text-blue-600 font-semibold" : ""}>Team</Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
