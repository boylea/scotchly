import scotchly
import unittest

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        scotchly.app.config['TESTING'] = True
        self.app = scotchly.app.test_client()

    def test_no_selection(self):
        rv = self.app.get('/')
        default_whisky = scotchly.app.config['DATA']['whiskynames'][0]
        selected_option = '<option selected="selected">{}</option>'.format(default_whisky)
        assert rv.status_code == 200
        assert selected_option in rv.data

    def test_selection(self):
        another_whisky = scotchly.app.config['DATA']['whiskynames'][7]
        rv = self.app.post('/', data={'whisky': another_whisky})
        selected_option = '<option selected="selected">{}</option>'.format(another_whisky)
        assert rv.status_code == 200
        assert selected_option in rv.data


if __name__ == '__main__':
    unittest.main()