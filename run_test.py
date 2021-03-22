from run import app
import unittest
from flask_pymongo import PyMongo


class FlaskTestCase(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/index', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_index_post(self):
        tester = app.test_client(self)
        response = tester.post(
            '/index_post', data={'title': 'Test Case', 'description': 'This is for the test case.'})
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_edit_topic(self):
        tester = app.test_client(self)
        topic = '6058f59a69110ec6df636972'
        response = tester.post('/edit_topic', query_string=topic, data={
                               'topic_title': 'Test Case', 'topic_description': 'This is for the test case.'})
        self.assertEqual(response.status_code, 302)

    def test_delete_topic(self):
        tester = app.test_client(self)
        topic = '6058f59a69110ec6df636972'
        response = tester.post('/delete_topic', query_string=topic)
        self.assertEqual(response.status_code, 302)


if __name__ == '__name__':
    unittest.main()
