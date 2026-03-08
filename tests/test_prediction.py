def test_predict(client):
    response = client.post(
        "/predict",
        json={
            "feature1": 2,
            "feature2": 3
        }
    )

    assert response.status_code == 200
    assert "prediction" in response.json()
    assert response.json()["prediction"] == 5.0