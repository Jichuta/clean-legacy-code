"""Item management CLI with secure authentication.

A demonstration of clean architecture, SOLID principles, and modern Python practices.
"""

import os
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path


class Command(Enum):
    ADD = "add"
    SHOW = "show"
    SAVE = "save"
    EXIT = "exit"


@dataclass
class Item:
    id: int
    value: str
    timestamp: str


class AuthenticationError(Exception):
    """Raised when authentication fails."""

    pass


class ItemRepository:
    """Handles item storage and retrieval."""

    def __init__(self, storage_path: str = "data.json") -> None:
        self._storage_path = Path(storage_path)
        self._items: list[Item] = []

    def add(self, value: str) -> Item:
        item_id = len(self._items) + 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item = Item(id=item_id, value=value, timestamp=timestamp)
        self._items.append(item)
        return item

    def get_all(self) -> list[Item]:
        return list(self._items)

    def save_to_file(self) -> None:
        with open(self._storage_path, "w", encoding="utf-8") as file:
            json.dump([asdict(item) for item in self._items], file, indent=2)

    def load_from_file(self) -> None:
        if self._storage_path.exists():
            with open(self._storage_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                self._items = [Item(**item_data) for item_data in data]


class Authenticator:
    """Handles user authentication using environment variables."""

    def __init__(self) -> None:
        self._username = os.environ.get("APP_USERNAME", "admin")
        self._password = os.environ.get("APP_PASSWORD", "")

    def authenticate(self, username: str, password: str) -> bool:
        return username == self._username and password == self._password


class ItemManager:
    """Coordinates item operations and user interaction."""

    def __init__(
        self, repository: ItemRepository, authenticator: Authenticator
    ) -> None:
        self._repository = repository
        self._authenticator = authenticator

    def run(self) -> None:
        self._authenticate_user()
        self._load_previous_items()
        self._interactive_loop()

    def _authenticate_user(self) -> None:
        username = input("User: ")
        password = input("Pass: ")
        if not self._authenticator.authenticate(username, password):
            raise AuthenticationError("Invalid credentials")

    def _load_previous_items(self) -> None:
        self._repository.load_from_file()

    def _interactive_loop(self) -> None:
        print("Welcome")
        commands = {cmd.value: cmd for cmd in Command}

        while True:
            cmd_input = input("What to do? (add/show/save/exit): ").strip().lower()
            if cmd_input == Command.EXIT.value:
                break

            command = commands.get(cmd_input)
            if command is None:
                print("Unknown command.")
                continue

            self._execute_command(command)

    def _execute_command(self, command: Command) -> None:
        if command == Command.ADD:
            value = input("Value: ")
            if not value:
                print("Value cannot be empty.")
                return
            self._repository.add(value)
            print("Added.")
        elif command == Command.SHOW:
            for item in self._repository.get_all():
                print(f"Item: {item.id} - {item.value} at {item.timestamp}")
        elif command == Command.SAVE:
            self._repository.save_to_file()
            print("Saved.")


def main() -> None:
    try:
        authenticator = Authenticator()
        repository = ItemRepository()
        manager = ItemManager(repository, authenticator)
        manager.run()
    except AuthenticationError as e:
        print("Wrong!")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
