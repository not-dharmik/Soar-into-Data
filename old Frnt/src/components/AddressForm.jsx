import { useState } from 'react';

function AddressForm({ onSubmit }) {
  const [input, setInput] = useState('');
  const [start, setStart] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const addresses = input.split('\n').map((a) => a.trim()).filter(Boolean);
    if (!addresses.includes(start)) {
      alert("Start address must be one of the input addresses.");
      return;
    }
    onSubmit({ addresses, start });
  };

  const inputAddresses = input.split('\n').map((a) => a.trim()).filter(Boolean);

  return (
    <form onSubmit={handleSubmit} className="mb-6">
      <label className="block mb-2 font-semibold text-gray-700">
        Enter Addresses (one per line):
      </label>
      <textarea
        rows={5}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        className="w-full p-3 border border-gray-300 rounded-xl shadow-sm resize-none"
        placeholder="123 Main St, Irvine, CA 92612"
      />
      {inputAddresses.length > 0 && (
        <>
          <label className="block mt-4 mb-2 font-semibold text-gray-700">
            Select Starting Address:
          </label>
          <select
            className="w-full p-2 border border-gray-300 rounded-xl"
            value={start}
            onChange={(e) => setStart(e.target.value)}
            required
          >
            <option value="">-- Choose --</option>
            {inputAddresses.map((addr, idx) => (
              <option key={idx} value={addr}>
                {addr}
              </option>
            ))}
          </select>
        </>
      )}
      <button
        type="submit"
        className="mt-4 px-6 py-3 bg-green-600 text-white rounded-xl hover:bg-green-700 transition-all"
      >
        Find Dynamic Route
      </button>
    </form>
  );
}

export default AddressForm;
