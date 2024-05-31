import os
import unittest

import __name__


class TestBaseWindow(unittest.TestCase):
    def setUp(self):
        self.window = __name__(None)

    def test_hash_password(self):
        password = "password123"
        hashed_password = self.window.hash_password(password)
        self.assertNotEqual(password, hashed_password)
        self.assertEqual(len(hashed_password), 64)

    def test_check_user(self):
        # Создаем временный файл с данными пользователей
        with open("test_users.txt", "w") as file:
            file.write("test_user,password123\n")

        self.assertTrue(self.window.check_user("test_user"))
        self.assertFalse(self.window.check_user("nonexistent_user"))

        # Удаляем временный файл
        os.remove("test_users.txt")

    def tearDown(self):
        del self.window
