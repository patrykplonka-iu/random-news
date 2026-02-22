import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from uuid import uuid4

from logic import ChatState, continue_chat, start_chat

HOST = "127.0.0.1"
PORT = 8000

sessions: dict[str, ChatState] = {}


class ApiHandler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            return {}
        raw = self.rfile.read(length) if length > 0 else b"{}"
        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            return {}

    def do_OPTIONS(self) -> None:
        self._send_json(HTTPStatus.NO_CONTENT, {})

    def do_GET(self) -> None:
        if self.path == "/api/health":
            self._send_json(HTTPStatus.OK, {"status": "ok"})
            return
        self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})

    def do_POST(self) -> None:
        if self.path == "/api/chat/start":
            body = self._read_json()
            name = str(body.get("name", "")).strip()
            if not name:
                self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Name is required"})
                return

            state, first_message = start_chat(name)
            session_id = str(uuid4())
            sessions[session_id] = state
            self._send_json(
                HTTPStatus.OK,
                {
                    "sessionId": session_id,
                    "botMessage": first_message,
                    "done": state["done"],
                },
            )
            return

        if self.path == "/api/chat/message":
            body = self._read_json()
            session_id = str(body.get("sessionId", "")).strip()
            user_message = str(body.get("message", ""))

            if not session_id:
                self._send_json(HTTPStatus.BAD_REQUEST, {"error": "sessionId is required"})
                return

            state = sessions.get(session_id)
            if state is None:
                self._send_json(HTTPStatus.NOT_FOUND, {"error": "Session not found"})
                return

            next_state, bot_message = continue_chat(state, user_message)
            sessions[session_id] = next_state
            self._send_json(
                HTTPStatus.OK,
                {
                    "botMessage": bot_message,
                    "done": next_state["done"],
                },
            )
            return

        self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})

    def log_message(self, format: str, *args) -> None:
        return


def run() -> None:
    server = ThreadingHTTPServer((HOST, PORT), ApiHandler)
    print(f"API running at http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
