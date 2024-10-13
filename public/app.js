// User registration (simplified without backend storage)
document.getElementById("signup-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  // Store user details in localStorage for demo purposes
  localStorage.setItem("user", JSON.stringify({ name, email, password }));

  alert("User registered successfully! Please log in.");
});

//  room ka logic
document.getElementById("create-room").addEventListener("click", () => {
  const roomName = document.getElementById("room-name").value;
  if (roomName) {
      const roomId = Math.random().toString(36).substring(2, 15);
      alert(`Room created: ${roomName}, ID: ${roomId}`);
      addRoomToList(roomName, roomId);
  } else {
      alert("Please enter a room name.");
  }
});

// room meh jane ka logic
document.getElementById("join-room-btn").addEventListener("click", () => {
  const roomId = document.getElementById("join-room").value;
  if (roomId) {
      alert(`Joined Room with ID: ${roomId}`);
      // Here you would connect the user to the room
  } else {
      alert("Please enter a room ID.");
  }
});

// Display room in the list
function addRoomToList(roomName, roomId) {
  const roomList = document.getElementById("room-list");
  const roomItem = document.createElement("div");
  roomItem.innerHTML = `<strong>${roomName}</strong> (ID: ${roomId})`;
  roomList.appendChild(roomItem);
}
