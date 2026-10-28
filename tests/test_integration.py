"""
End-to-End Integration and Edge Case Validation Suite
"""
import requests
import json

base = "http://127.0.0.1:8000"

print("--- Step 1: Health & Discovery ---")
r_root = requests.get(base + "/")
assert r_root.status_code == 200
print("Root API online:", r_root.json()["status"])

r_health = requests.get(base + "/health")
assert r_health.status_code == 200
print("System Health:", r_health.json()["status"])

print("\n--- Step 2: Authentication Workflow ---")
reg_data = {
    "username": "AgriAdmin2026",
    "email": "admin2026@agriyield.org",
    "password": "SecureAgriPassword123!"
}
r_reg = requests.post(base + "/register", json=reg_data)
if r_reg.status_code == 400:
    r_reg = requests.post(base + "/login", json={"username": reg_data["username"], "password": reg_data["password"]})

assert r_reg.status_code == 200, f"Auth failed: {r_reg.text}"
token = r_reg.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print(f"Authenticated successfully as: {reg_data['username']}")

r_me = requests.get(base + "/auth/me", headers=headers)
assert r_me.status_code == 200
assert r_me.json()["username"] == reg_data["username"]
print(f"Verified profile: {r_me.json()['email']}")

print("\n--- Step 3: Multi-Season Predictions with Real ML Pipelines ---")
test_queries = [
    {
        "season": "Kharif",
        "continent": "Asia",
        "area": "India",
        "crop": "Maize",
        "year": 2026,
        "average_rain_fall_mm_per_year": 1200.0,
        "pesticides_tonnes": 500.0,
        "avg_temp": 25.0
    },
    {
        "season": "Rabi",
        "continent": "Asia",
        "area": "India",
        "crop": "Wheat",
        "year": 2026,
        "average_rain_fall_mm_per_year": 650.0,
        "pesticides_tonnes": 300.0,
        "avg_temp": 18.0
    },
    {
        "season": "Seasonal",
        "continent": "Asia",
        "area": "India",
        "crop": "Rice, paddy",
        "year": 2026,
        "average_rain_fall_mm_per_year": 1400.0,
        "pesticides_tonnes": 600.0,
        "avg_temp": 27.0
    }
]

for q in test_queries:
    res = requests.post(base + "/predict", json=q, headers=headers)
    assert res.status_code == 200, f"Prediction failed: {res.text}"
    p = res.json()
    print(f"[{p['season']}] {p['crop']} in {p['country']} -> Predicted: {p['predicted_yield_hg_per_ha']:,.2f} hg/ha | Potential: {p['potential_score']}/100 ({p['potential_rating']}) | Model: {p['model_used']}")

print("\n--- Step 4: User-Specific Prediction History ---")
h_res = requests.get(base + "/history", headers=headers)
assert h_res.status_code == 200
h_data = h_res.json()
print(f"User history retrieved: {h_data['count']} records found.")
assert h_data['count'] >= 3

print("\n--- Step 5: Analytics and Model Comparison Verification ---")
sum_res = requests.get(base + "/analytics/summary")
assert sum_res.status_code == 200
s_data = sum_res.json()
print(f"Global Summary: {s_data['total_records']:,} records across {s_data['total_countries']} countries and {s_data['total_crops']} crops.")

mc_res = requests.get(base + "/model-comparison")
assert mc_res.status_code == 200
mc_data = mc_res.json()
print(f"Model Comparison: {len(mc_data['evaluation_results'])} benchmark evaluations verified.")

print("\n--- Step 6: Negative & Edge Case Validation ---")
bad_season = requests.post(base + "/predict", json={**test_queries[0], "season": "UnknownSeason"}, headers=headers)
assert bad_season.status_code == 404, "Expected 404 for unknown season"
print("[PASS] Unknown season correctly rejected with 404")

bad_crop = requests.post(base + "/predict", json={**test_queries[0], "crop": "InvalidCrop"}, headers=headers)
assert bad_crop.status_code == 400, "Expected 400 for invalid crop"
print("[PASS] Incompatible crop correctly rejected with 400")

no_auth = requests.post(base + "/predict", json=test_queries[0])
assert no_auth.status_code == 401, "Expected 401 for unauthorized access"
print("[PASS] Protected endpoint correctly protected with 401")

bad_login = requests.post(base + "/login", json={"username": "AgriAdmin2026", "password": "WrongPassword"})
assert bad_login.status_code == 401, "Expected 401 for bad login"
print("[PASS] Invalid credentials correctly rejected with 401")

print("\n=======================================================")
print("ALL END-TO-END INTEGRATION TESTS PASSED 100% SUCCESSFULLY!")
print("=======================================================")
