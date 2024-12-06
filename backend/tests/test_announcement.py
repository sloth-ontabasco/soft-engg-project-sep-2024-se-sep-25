import unittest
from unittest.mock import patch
from mongomock import MongoClient
from src.app_factory import setup_app
from src.models.announcement import Announcement
from src.models.project import Project
from src.models.user import User

class TestAnnouncementAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('fskdhfkjsdbfks sdfhjl')
        cls.app = setup_app()
        cls.client =cls.app.test_client()

        # Mock MongoDB
        cls.mongo_client = MongoClient()
        cls.db = cls.mongo_client['testdb']

        # Mock collections
        cls.announcements = cls.db['announcement']
        cls.projects = cls.db['project']
        cls.users = cls.db['user']

        # Patch the db connection
        cls.patcher = patch('src.models.announcement.db', cls.db)
        cls.patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.patcher.stop()
        cls.mongo_client.drop_database('testdb')

    def setUp(self):
        self.project = Project(title="Test Project", description="Test Description")
        self.project.save()
        self.user = User(username="testuser", email="test@example.com",role="student")
        # self.user.save()
        self.announcement = Announcement(
            project=self.project,
            title="Test Announcement",
            content="Test Content",
            posted_by=self.user
        )
        # self.announcement.save()

    def tearDown(self):
        pass
    def test_get_all_announcements(self):
        response = self.client.get(f'/api/projects/{self.project.id}/announcements')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertTrue(data['success'])
        self.assertEqual(len(data['announcements']), 1)
        self.assertEqual(data['announcements'][0]['title'], "Test Announcement")

    def test_get_announcement_by_id(self):
        response = self.client.get(f'/api/projects/{self.project.id}/announcements/{self.announcement.id}')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertTrue(data['success'])
        self.assertEqual(data['announcement']['title'], "Test Announcement")

    def test_post_announcement(self):
        response = self.client.post(
            f'/api/projects/{self.project.id}/announcements',
            json={
                'title': 'New Announcement',
                'content': 'New Content'
            },
            headers={'Authorization': f'Bearer {self.user.create_access_token()}'}
        )
        self.assertEqual(response.status_code, 201)
        data = response.json
        self.assertTrue(data['success'])
        self.assertEqual(data['announcement']['title'], 'New Announcement')

    def test_put_announcement(self):
        response = self.client.put(
            f'/api/projects/{self.project.id}/announcements/{self.announcement.id}',
            json={
                'title': 'Updated Announcement'
            },
            headers={'Authorization': f'Bearer {self.user.create_access_token()}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertTrue(data['success'])
        self.assertEqual(data['announcement']['title'], 'Updated Announcement')

    def test_delete_announcement(self):
        response = self.client.delete(
            f'/api/projects/{self.project.id}/announcements/{self.announcement.id}',
            headers={'Authorization': f'Bearer {self.user.create_access_token()}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Announcement deleted')

if __name__ == '__main__':
    with patch('sys.argv', ['test_announcement.py']):
        unittest.main()