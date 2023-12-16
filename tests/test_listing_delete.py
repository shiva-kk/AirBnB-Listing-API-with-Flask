import unittest
from app import app

class TestDeleteListingEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        # Add any setup steps if needed

    def test_delete_listing_success(self):
        listing_id = 78035

        response = self.app.delete(f'/listing/{listing_id}')
        self.assertEqual(response.status_code, 200) 
       

    def test_delete_listing_not_found(self):
        invalid_listing_id = 999

        response = self.app.delete(f'/listing/{invalid_listing_id}')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)

    def test_delete_listing_bad_request(self):
        invalid_data = "test"

        response = self.app.delete('/listing/1', json=invalid_data)
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)

if __name__ == '__main__':
    unittest.main()

