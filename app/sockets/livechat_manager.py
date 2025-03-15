from typing import Any, Dict, Optional, cast
from dataclasses import dataclass
import logging
from flask import request
from flask_socketio import emit, join_room, SocketIO

# Configure module-level logger
logger = logging.getLogger(__name__)

PASTOR_ROOM = "pastor_room"


def get_sid() -> str:
    """
    Retrieve the SocketIO session ID from the Flask request object.
    """
    return cast(str, getattr(request, "sid", ""))


@dataclass
class ClientInfo:
    """
    Data class to store client connection details.
    """
    user_type: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    room: Optional[str] = None


class LiveChatManager:
    """
    Manages SocketIO live chat events.
    """
    def __init__(self) -> None:
        self.clients: Dict[str, ClientInfo] = {}
        self.pastor_online: bool = False
        self.pastor_sid: Optional[str] = None

    def broadcast_pastor_status(self, status: str) -> None:
        """
        Broadcast the pastor's status (online/offline) to all clients.
        """
        emit("pastor_status", {"status": status}, broadcast=True)  # type: ignore

    def handle_connect(self) -> None:
        """
        Handle new client connections.
        """
        sid = get_sid()
        user_type = request.args.get("user_type", "user")
        if user_type == "pastor":
            self.clients[sid] = ClientInfo(user_type="pastor")
            self.pastor_online = True
            self.pastor_sid = sid
            join_room(PASTOR_ROOM)  # type: ignore
            self.broadcast_pastor_status("online")
            logger.info("Pastor connected with SID: %s", sid)
        else:
            name = request.args.get("name", "Anonymous")
            email = request.args.get("email", "")
            phone = request.args.get("phone", "")
            user_room = f"user_{sid}"
            self.clients[sid] = ClientInfo(
                user_type="user", name=name, email=email, phone=phone, room=user_room
            )
            join_room(user_room)  # type: ignore
            # Inform the user about pastor status
            emit("pastor_status", {"status": "online" if self.pastor_online else "offline"})
            if self.pastor_sid:
                user_info = {
                    "user_id": sid,
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "room": user_room,
                    "status": "connected",
                }
                emit("user_connected", user_info, room=PASTOR_ROOM)  # type: ignore
            logger.info("User connected with SID: %s, room: %s", sid, user_room)

    def handle_disconnect(self) -> None:
        """
        Handle client disconnections.
        """
        sid = get_sid()
        client = self.clients.pop(sid, None)
        if not client:
            return

        if client.user_type == "pastor":
            self.pastor_online = False
            self.pastor_sid = None
            self.broadcast_pastor_status("offline")
            logger.info("Pastor disconnected with SID: %s", sid)
        else:
            if self.pastor_sid:
                disconnect_info = {
                    "user_id": sid,
                    "name": client.name or "Anonymous",
                    "status": "disconnected",
                }
                emit("user_disconnected", disconnect_info, room=PASTOR_ROOM)  # type: ignore
            logger.info("User disconnected with SID: %s", sid)

    def handle_chat_message(self, data: Dict[str, Any]) -> None:
        """
        Handle incoming chat messages.
        """
        sid = get_sid()
        sender = self.clients.get(sid)
        if not sender:
            return

        message = {
            "msg": data.get("msg", ""),
            "timestamp": data.get("timestamp", "")
        }

        if sender.user_type == "pastor":
            target_user_id = data.get("target_user_id")
            if target_user_id and target_user_id in self.clients:
                user_room = self.clients[target_user_id].room
                if user_room:
                    message.update({"sender": "Pastor", "user_type": "pastor"})
                    emit("chat_message", message, room=user_room)  # type: ignore
                    # Additional info for pastor UI
                    message.update({
                        "recipient": self.clients[target_user_id].name or "Anonymous",
                        "target_user_id": target_user_id,
                    })
                    emit("chat_message", message, room=PASTOR_ROOM)  # type: ignore
                    logger.info("Pastor sent message to user %s", target_user_id)
        else:
            if self.pastor_sid:
                message.update({
                    "sender": sender.name or "Anonymous",
                    "user_type": "user",
                    "user_id": sid,
                    "email": sender.email or "",
                    "phone": sender.phone or "",
                })
                emit("chat_message", message, room=PASTOR_ROOM)  # type: ignore
                emit("chat_message", message, room=sender.room)  # type: ignore
                logger.info("User %s sent message; forwarded to pastor.", sid)

    def register_events(self, socketio: SocketIO) -> None:
        """
        Register SocketIO event handlers.
        """
        socketio.on_event("connect", self.handle_connect)  # type: ignore
        socketio.on_event("disconnect", self.handle_disconnect)  # type: ignore
        socketio.on_event("chat_message", self.handle_chat_message)  # type: ignore
        logger.info("LiveChatManager events registered.")


# Global instance for reuse across the application
livechat_manager = LiveChatManager()
