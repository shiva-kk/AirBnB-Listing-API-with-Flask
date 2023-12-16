import unittest
from app import app

class TestListingsEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        # Add any setup steps if needed

    def test_get_all_listings_success(self):
        response = self.app.get('/listings')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_listing_by_id_not_found(self):
        response = self.app.get('/listings/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)

    def test_get_listings_filtered_success(self):
        response = self.app.get('/listings?price_gt=50&price_lt=150&neighborhood=78702')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)


if __name__ == '__main__':
    unittest.main()
