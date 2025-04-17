import { useState } from "react";

function AddressForm({ setRouteData, setMode }) {
  const [input, setInput] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const addresses = input.split("\n").map((a) => a.trim()).filter(Boolean);
    const res = await fetch("http://localhost:8000/dynamic-route", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ addresses })
    });
    const data = await res.json();
    setMode("dynamic");
    setRouteData(data);
  };

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        rows={6}
        className="w-full p-2 border rounded mb-2"
        placeholder="Enter addresses line-by-line..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button
        type="submit"
        className="bg-green-600 text-white px-4 py-2 rounded"
      >
        Get Dynamic Route
      </button>
    </form>
  );
}

export default AddressForm;
