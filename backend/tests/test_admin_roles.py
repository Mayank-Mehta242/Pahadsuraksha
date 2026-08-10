import unittest

from routes.admin import is_official_role


class OfficialRoleTests(unittest.TestCase):
    def test_accepts_common_official_role_variants(self):
        self.assertTrue(is_official_role("Official"))
        self.assertTrue(is_official_role("Admin"))
        self.assertTrue(is_official_role("Disaster Official/RoadManagement"))

    def test_rejects_citizen_role(self):
        self.assertFalse(is_official_role("Citizen"))


if __name__ == "__main__":
    unittest.main()
