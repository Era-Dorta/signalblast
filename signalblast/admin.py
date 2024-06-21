import os
from typing import Optional

import bcrypt

from signalblast.utils import get_code_data_path


class Admin:
    save_path = get_code_data_path() / "admin.txt"

    def __init__(self) -> None:
        self.admin_id: str = None
        self._hashed_password: str = None

    @classmethod
    async def create(cls, admin_password: Optional[str]) -> None:
        self = Admin()
        self.admin_id = None
        await self.set_hashed_password(admin_password)
        return self

    def get_hashed_password(self):
        return self._hashed_password

    async def set_hashed_password(self, password: str):
        if password is None:
            self._hashed_password = "".encode()
        else:
            self._hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        await self.save_to_file()

    async def add(self, id: str, admin_password: Optional[str]) -> bool:
        if admin_password is None:
            return False

        if bcrypt.checkpw(admin_password.encode(), self.get_hashed_password()):
            self.admin_id = id
            await self.save_to_file()
            return True
        else:
            return False

    async def remove(self, admin_password: Optional[str]) -> bool:
        if admin_password is None:
            return False

        if bcrypt.checkpw(admin_password.encode(), self.get_hashed_password()):
            self.admin_id = None
            await self.save_to_file()
            return True
        else:
            return False

    async def save_to_file(self) -> None:
        with open(self.save_path, "w") as f:
            if self.admin_id is None:
                f.write("\n")
            else:
                f.write(self.admin_id + "\n")
            f.write(self.get_hashed_password().decode())

    @staticmethod
    async def _load_from_file() -> "Admin":
        admin = Admin()
        with open(Admin.save_path, "r") as f:
            admin.admin_id = f.readline().rstrip()
            admin._hashed_password = f.readline().encode()

        if admin.admin_id == "":
            admin.admin_id = None

        return admin

    @staticmethod
    async def load_from_file(admin_password: Optional[str]) -> "Admin":
        if not os.path.exists(Admin.save_path):
            return await Admin.create(admin_password)

        admin = await Admin._load_from_file()
        # Overwrite the password in the file, if no password was given assume we want to keep the one from the file
        if admin_password is not None:
            await admin.set_hashed_password(admin_password)
        return admin
