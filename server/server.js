const { Server } = require("socket.io");

const io = new Server(3000, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"],
  },
});

console.log("Servidor Socket.IO rodando na porta 3000");

io.on("connection", (socket) => {
  console.log("Cliente conectado:", socket.id);

  socket.emit("server_message", "Bem-vindo ao servidor Socket.IO!");

  socket.on("client_message", (data) => {
    console.log("message:", data);
  });

  socket.on("disconnect", () => {
    console.log("Cliente desconectado:", socket.id);
  });
});
