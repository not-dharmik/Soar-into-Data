const teamMembers = [
    {
      name: "Dharmik",
      image: "https://via.placeholder.com/100",
      linkedin: "#",
      role: "Data Science @ UCI",
    },
    {
      name: "Teammate 2",
      image: "https://via.placeholder.com/100",
      linkedin: "#",
      role: "Frontend Developer",
    },
    {
      name: "Teammate 3",
      image: "https://via.placeholder.com/100",
      linkedin: "#",
      role: "API Integrator",
    },
  ];
  
  function Team() {
    return (
      <div className="max-w-5xl mx-auto mt-12">
        <h2 className="text-3xl font-bold text-center mb-6 text-purple-800">Meet Our Team</h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          {teamMembers.map((member, idx) => (
            <div key={idx} className="bg-white p-4 rounded-xl shadow text-center">
              <img src={member.image} alt={member.name} className="mx-auto w-24 h-24 rounded-full mb-3" />
              <h3 className="text-lg font-semibold text-gray-800">{member.name}</h3>
              <p className="text-gray-600">{member.role}</p>
              <a href={member.linkedin} className="text-blue-500 hover:underline" target="_blank" rel="noreferrer">
                LinkedIn
              </a>
            </div>
          ))}
        </div>
      </div>
    );
  }
  
  export default Team;
  