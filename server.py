import socket
import threading
from setting import Settings
from level import Level
import json


class Server:
    def __init__(self, setting):
        self.setting = setting
        self.setting.random_seed = 0
        self.host = "0.0.0.0"
        self.port = setting.server_port
        self.addr_clients = {}  # 存储地址和客户端
        self.username_addr = {} # 存储用户名和地址
        self.addr_username =  {}  # 存储地址和用户名
        self.username_roomnumber = {}  # 存储用户名和房间号
        self.rooms = {}  # 存储房间信息
        self.lock = threading.Lock()  # 用于线程安全访问共享资源

    def process_client_message(self, message, addr):
        """处理客户端消息 - 这里可以实现具体的游戏逻辑"""
        if message.startswith("***###*#*###***"):  # 注册信息
            room_number = message.split("***###*#*###***")[2]
            user_name = message.split("***###*#*###***")[1]
            print(message.split("***###*#*###***"))
            self.username_roomnumber[user_name] = room_number
            self.username_addr[user_name] = addr
            self.addr_username[addr] = user_name
            if room_number not in self.rooms:
                self.rooms[room_number] = {"players": {}, "scores": {}, "level": Level(self.setting)}
                self.rooms[room_number]["level"].generate_maze()
            self.rooms[room_number]["players"][user_name] = False
            # self.flush_room(room_number)
            if len(self.rooms[room_number]["players"]) == 2:
                self.start_room(room_number)
        else:
            user_name = self.addr_username[addr]
            room_number = self.username_roomnumber[user_name]
            self.rooms[room_number]["scores"][user_name] = message
            if len(self.rooms[room_number]["scores"]) == 2:
                self.score_room(room_number)
        # elif message.startswith("*#*###*#*###***"):  # 准备好了
        #     user_name = self.addr_username[addr]
        #     room_number = self.username_roomnumber[user_name]
        #     self.rooms[room_number]["players"][user_name] = True
        #     self.flush_room(room_number)
        #     all_ready = False
        #     # for username, is_ready in self.rooms[room_number]["players"]:
        #     #     if not is_ready:
        #     #         all_ready = False
        #     #         break
        #     #     all_ready = True
        #     if len(self.rooms[room_number]["players"] == 2): all_ready = True  # 测试
        #     if all_ready:
        #         self.start_room(room_number)

    def start_room(self, room_number):
        for username in self.rooms[room_number]["players"]:
            self.addr_clients[self.username_addr[username]].send(self.rooms[room_number]["level"].to_dict_string().encode("utf-8"))

    def score_room(self, room_number):
        for username in self.rooms[room_number]["scores"].keys():
            for i in self.rooms[room_number]["scores"].keys():
                if i != username:
                    score = self.rooms[room_number]["scores"][i]
                    break
            self.addr_clients[self.username_addr[username]].send(str(score).encode("utf-8"))
        self.rooms.pop(room_number)

    def flush_room(self, room_number):
        r = self.rooms[room_number]
        for username in self.rooms[room_number]["players"]:
            self.addr_clients[self.username_addr[username]].send(("r"+json.dumps(r)).encode("utf-8"))

    def handle_client(self, client_socket, addr):
        """处理单个客户端的连接"""
        print(f"Client {addr} connected")

        try:
        # client_socket.send("OK".encode("utf-8"))

            # 持续接收来自客户端的消息
            while True:
                data = client_socket.recv(65536).decode("utf-8")
                if not data:
                    break

                print(f"Received data from {addr}: {data}")

                # 处理客户端发送的数据（这里可以根据实际协议添加处理逻辑）
                response = self.process_client_message(data, addr)

                # 如果有响应数据，则发送给客户端
                if response:
                    print(f"Sending response to {addr}: {response}")
                    client_socket.send(response.encode("utf-8"))

        except ConnectionResetError:
            print(f"Client {addr} disconnected unexpectedly")
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
        finally:
            # 清理客户端连接
            with self.lock:
                if addr in self.addr_clients:
                    del self.addr_clients[addr]
                    del self.username_addr[self.addr_username[addr]]
                    del self.username_roomnumber[self.addr_username[addr]]
                    del self.addr_username[addr]
            client_socket.close()
            print(f"Client {addr} disconnected")

    def accept_connections(self):
        """接受新的客户端连接"""
        server_socket = socket.socket()
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print("Listening from", self.host, "on port", self.port, "...")

        try:
            while True:
                client_socket, addr = server_socket.accept()

                # 将客户端添加到连接列表
                with self.lock:
                    self.addr_clients[addr] = client_socket

                print(f"Got connection from {addr}, total clients: {len(self.addr_clients)}")

                # 为每个客户端创建一个新线程
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, addr),
                    daemon=True  # 设置为守护线程
                )
                client_thread.start()

        except KeyboardInterrupt:
            print("\nShutting down server...")
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            server_socket.close()

    def run(self):
        """启动服务器"""
        print("Starting multi-threaded server...")
        self.accept_connections()


def main():
    setting = Settings()
    server = Server(setting)
    server.run()


if __name__ == "__main__":
    main()
