import unittest
from unittest.mock import MagicMock, patch

from app import app


class WeatherRouteTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch("routes.weather.requests.get")
    def test_returns_fallback_weather_when_openweather_fails(self, mock_get):
        current_response = MagicMock(status_code=401)
        current_response.json.return_value = {"cod": 401, "message": "Invalid API key"}
        forecast_response = MagicMock(status_code=401)
        forecast_response.json.return_value = {"cod": 401, "message": "Invalid API key"}
        mock_get.side_effect = [current_response, forecast_response]

        response = self.client.get("/api/weather/?city=Tehri")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["city"], "Tehri")
        self.assertEqual(payload["condition"], "Weather unavailable")
        self.assertEqual(payload["roadStatus"]["level"], "Safe")


if __name__ == "__main__":
    unittest.main()
