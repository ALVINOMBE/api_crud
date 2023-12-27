import unittest
import json
from api import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

    def test_add_customer(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "middle_name": "M",
            "gender": "Male",
            "email": "john.doe@example.com",
            "street_address": "123 Main St",
            "city": "Cityville",
            "country": "Countryland"
        }

        response = self.app.post('/customer', json=data)
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["message"], "customer added successfully")

    def test_add_customer_missing_fields(self):
        data = {
            "last_name": "Doe",
            "gender": "Male",
            "email": "john.doe@example.com",
            "street_address": "123 Main St",
            "city": "Cityville",
            "country": "Countryland"
        }

        response = self.app.post('/customer', json=data)
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 400)
        self.assertIn("Error", data)
        
    def test_update_customer(self):
        data = {
            "first_name": "Updated",
            "last_name": "Doe",
            "middle_name": "M",
            "gender": "Male",
            "email": "john.doe@example.com",
            "street_address": "123 Main St",
            "city": "Cityville",
            "country": "Countryland"
        }

        response = self.app.put('/customer/1', json=data)
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "customer updated successfully")

    def test_update_customer_invalid_data(self):
        data = {
            "first_name": "Updated",
            "last_name": "Doe",
            "middle_name": "M",
            "gender": "Male",
            "email": "john.doe@example.com",
            "street_address": "123 Main St",
            "city": "Cityville",
            "country": "Countryland"
        }

        response = self.app.put('/customer/33', json=data)
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 500)
        self.assertIn("Error", data)
        
if __name__ == '__main__':
    unittest.main()