import unittest
from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_shows(self):
        response = self.app.get('/api/shows')
        self.assertEqual(response.status_code, 200)

    def test_create_show(self):
        data = {
            'venue_id': 1,
            'name': 'Test Show',
            'rating': 4,
            'start_time': '2025-01-01 12:00:00',
            'end_time': '2025-01-01 14:00:00',
            'price': 50.0,
            'tags': 'test, show'
        }
        response = self.app.post('/api/shows', json=data)
        self.assertEqual(response.status_code, 201)

    def test_get_venues(self):
        response = self.app.get('/api/venues')
        self.assertEqual(response.status_code, 200)

    def test_create_venue(self):
        data = {
            'name': 'Test Venue',
            'address': '123 Test St',
            'city': 'Test City',
            'capacity': 100,
        }
        response = self.app.post('/api/venues', json=data)
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()