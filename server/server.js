const { Server } = require("socket.io");

const io = new Server(3000, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"],
  },
});

console.log("Servidor Socket.IO rodando na porta 3000");

const clients = {}; // Armazena os clientes conectados

io.on("connection", (socket) => {
  console.log("Cliente conectado:", socket.id);

  // Armazena o cliente no objeto
  clients[socket.id] = { id: socket.id };

  // // Envia mensagem de boas-vindas
  // socket.emit("server_message", "Bem-vindo ao servidor Socket.IO!");

  // Envia lista de clientes conectados para o cliente que solicitou
  socket.on("get_clients", () => {
    const otherClients = Object.keys(clients).filter((id) => id !== socket.id);
    socket.emit("client_list", otherClients);
  });

  // Mensagem privada para um cliente específico
  socket.on("private_message", ({ to, message }) => {
    if (clients[to]) {
      io.to(to).emit("private_message", {
        from: socket.id,
        message,
      });
    } else {
      socket.emit("error", "Cliente não encontrado ou desconectado");
    }
  });

  socket.on("command_sent", ({ to, command }) => {
    if (clients[to]) {
      io.to(to).emit("command_received", {
        from: socket.id,
        command,
      });
    } else {
      socket.emit("error", "Cliente não encontrado ou desconectado");
    }
  });

  socket.on("frame_share", ({ to, image }) => {
    if (clients[to]) {
      io.to(to).emit("receive_image", {
        from: socket.id,
        image,
      });
    } else {
      socket.emit("error", "Cliente não encontrado ou desconectado");
    }
  });
  // Broadcast para todos os clientes (exceto o remetente)
  socket.on("client_message", (data) => {
    socket.broadcast.emit("broadcast_message", `Broadcast: ${data}`);
  });

  socket.on("prank", ({ to, prank }) => {
    if (clients[to]) {
      io.to(to).emit("prank", {
        from: socket.id,
        prank,
      });
      console.log("prank", prank);
    } else {
      socket.emit("error", "Cliente não encontrado ou desconectado");
    }
  });

  // Remove o cliente do registro ao desconectar
  socket.on("disconnect", () => {
    console.log("Cliente desconectado:", socket.id);
    delete clients[socket.id];
  });
});
