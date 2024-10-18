const net = require('net')

const handleConnection = socket => {
    console.log('Alguem se conectou.')
    socket.on('data',  data=> {
        console.log(data.toString())
    })
}

const server = net.createServer(handleConnection)

server.listen(4000, '127.0.0.1')