import unittest

from routes.prediction import get_coordinates


class TehriRouteTests(unittest.TestCase):
    def test_known_tehri_places_resolve_to_coordinates(self):
        candidates = [
            "Tehri",
            "New Tehri",
            "Chamba",
            "Dharasu",
            "Ghansali",
            "Narendranagar",
            "Bhatwari",
            "Devprayag",
            "Pratapnagar",
            "Jakhnidhar",
            "Kirtinagar",
            "Mansuna",
            "Miyuna",
            "Bhilangana"
        ]

        for place in candidates:
            self.assertIsNotNone(
                get_coordinates(place),
                msg=f"Expected {place} to resolve to coordinates"
            )


if __name__ == "__main__":
    unittest.main()
