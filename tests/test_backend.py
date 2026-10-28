import unittest
import time
from pathlib import Path
import sys

# Ensure backend can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from Backend.main import app


class BackendTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "online")
        self.assertIn("seasons_loaded", data)

    def test_02_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["database"], "connected")

    def test_03_get_seasons(self):
        response = self.client.get("/seasons")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("Kharif", data["seasons"])
        self.assertIn("Rabi", data["seasons"])
        self.assertIn("Seasonal", data["seasons"])

    def test_04_get_options_valid(self):
        response = self.client.get("/options?season=Kharif")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("continents", data)
        self.assertIn("Asia", data["continents"])
        self.assertIn("hierarchy", data)
        self.assertIn("India", data["hierarchy"]["Asia"])

    def test_05_get_options_invalid(self):
        response = self.client.get("/options?season=InvalidSeason")
        self.assertEqual(response.status_code, 404)

    def test_06_auth_and_prediction_flow(self):
        # 1. Register a test user
        username = f"user_{int(time.time()*1000)}"
        email = f"{username}@test.com"
        reg_res = self.client.post("/register", json={
            "username": username,
            "email": email,
            "password": "Password123!"
        })
        self.assertEqual(reg_res.status_code, 200)
        token = reg_res.json()["access_token"]
        self.assertTrue(bool(token))

        headers = {"Authorization": f"Bearer {token}"}

        # 2. Test /auth/me
        me_res = self.client.get("/auth/me", headers=headers)
        self.assertEqual(me_res.status_code, 200)
        self.assertEqual(me_res.json()["username"], username)

        # 3. Test /predict without token (should fail with 401)
        pred_payload = {
            "season": "Kharif",
            "continent": "Asia",
            "area": "India",
            "crop": "Maize",
            "year": 2026,
            "average_rain_fall_mm_per_year": 1200.0,
            "pesticides_tonnes": 500.0,
            "avg_temp": 25.0
        }
        no_auth = self.client.post("/predict", json=pred_payload)
        self.assertEqual(no_auth.status_code, 401)

        # 4. Test /predict with valid token
        pred_res = self.client.post("/predict", json=pred_payload, headers=headers)
        self.assertEqual(pred_res.status_code, 200)
        pred_data = pred_res.json()
        self.assertTrue(pred_data["success"])
        self.assertGreater(pred_data["predicted_yield_hg_per_ha"], 0)
        self.assertIn("potential_score", pred_data)
        self.assertIn("potential_rating", pred_data)
        self.assertIn("factors_impact", pred_data)

        # 5. Test /history
        hist_res = self.client.get("/history", headers=headers)
        self.assertEqual(hist_res.status_code, 200)
        hist_data = hist_res.json()
        self.assertGreaterEqual(hist_data["count"], 1)
        self.assertEqual(hist_data["history"][0]["crop"], "Maize")

    def test_07_analytics_and_models(self):
        res_summary = self.client.get("/analytics/summary")
        self.assertEqual(res_summary.status_code, 200)
        self.assertGreater(res_summary.json()["total_records"], 0)

        res_crops = self.client.get("/analytics/crops")
        self.assertEqual(res_crops.status_code, 200)
        self.assertGreater(len(res_crops.json()["data"]), 0)

        res_models = self.client.get("/model-comparison")
        self.assertEqual(res_models.status_code, 200)
        self.assertGreater(len(res_models.json()["evaluation_results"]), 0)


if __name__ == '__main__':
    unittest.main()
