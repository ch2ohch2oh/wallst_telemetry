const express = require("express");
const app = express();

app.use(express.static("static"));

const http = require("http");
const server = http.createServer(app);

const io = require("socket.io")(server);

const kafka = require("kafka-node");
const kafkaClient = new kafka.KafkaClient({
  kafkaHost: process.env.KAFKA_HOST || "localhost:9093",
});
const kafkaConsumer = new kafka.Consumer(kafkaClient, [{ topic: "comments" }]);

kafkaConsumer.on("message", function (comment) {
  comment = comment.value;
  //   console.log(comment);
  io.emit("comment", comment);
});

app.get("/", (req, res) => {
  res.sendFile(__dirname + "/static/html/index.html");
});

io.on("connection", (socket) => {
  //   console.log("User connected at: " + socket);
  socket.on("disconnect", () => {
    // console.log("User disconnected at: " + socket);
  });
});

const port = process.env.PORT || 3000;

server.listen(port, () => {
  console.log(`Server started at port ${port}`);
});
