from flask_testing import TestCase
from consumer.consumer_app import consumer

class TestConsumer(TestCase):

    def create_app(self):
        self.client = consumer.test_client()
        return consumer
    
    def test_root(self):
        self.client.get('/')
        self.assert_template_used('login.html')

    def test_invalid_route(self):
        self.client.get('/authorize')
        self.assert_template_used('40x.html')

    def test_wrong_creds_authorize(self):
        self.client.post('/authorize',data={"user_name":"test","password":"test"})
        self.assert_template_used('login.html')

    def test_noauth_list(self):
        self.client.post('/list',data={"user_name":"test"})
        self.assert_template_used('login.html')

    def test_noauth_new_resorce(self):
        self.client.post('/new_resource',data={"user_name":"test"})
        self.assert_template_used('login.html')

    def test_noauth_details(self):
        self.client.post('/details',data={"user_name":"test"})
        self.assert_template_used('login.html')

    def test_noauth_add_details(self):
        self.client.post('/add_details',data={"user_name":"test"})
        self.assert_template_used('login.html')

    def test_noauth_update_resource(self):
        self.client.post('/update_resource',data={"user_name":"test"})
        self.assert_template_used('login.html')

    def test_noauth_update_details(self):
        self.client.post('/update_details',data={"user_name":"test"})
        self.assert_template_used('login.html')
    
    def test_noauth_delete_details(self):
        self.client.post('/delete_details',data={"user_name":"test"})
        self.assert_template_used('login.html')

    def test_logout(self):
        self.client.post('/logout',data={"user_name":"test"})
        self.assert_template_used('login.html')

    def test_valid_authorize(self):
        self.client.post('/authorize',data={"user_name":"janedoe","password":"secret"})
        self.assert_template_used('list.html')
        print(self.get_context_variable("resources"))
        assert len(self.get_context_variable("resources")) != 0
        self.assert_context("username", "janedoe")

    def setUp(self):
        self.client.post('/authorize',data={"user_name":"janedoe","password":"secret"})

    def test_read_details(self):
        self.client.post('/details',data={"user_name":"janedoe","resource_id":"1001"})
        self.assert_template_used('details.html')
        self.assert_context("display_type", "view")
        self.assert_context("username", "janedoe")

    def test_new_resource(self):
        self.client.post('/new_resource',data={"user_name":"janedoe"})
        self.assert_template_used('details.html')
        self.assert_context("display_type", "new")
        self.assert_context("username", "janedoe")

    def test_add_details(self):
        self.client.post('/add_details',data={"user_name":"janedoe","resource_id":"1212","resource_name":"Rose","resource_type":"Plant","is_endangered":"False"})
        self.assert_template_used('details.html')
        self.assert_context("display_type", "view")
        self.assert_context("username", "janedoe")

    def test_update_resource(self):
        self.client.post('/update_resource',data={"user_name":"janedoe","resource_id":"1212"})
        self.assert_template_used('details.html')
        self.assert_context("display_type", "update")
        self.assert_context("username", "janedoe")

    def test_update_details(self):
        self.client.post('/update_details',data={"user_name":"janedoe","resource_id":1212,"resource_name":"Rose","resource_type":"Plant","is_endangered":False})
        self.assert_template_used('details.html')
        self.assert_context("display_type", "view")
        self.assert_context("username", "janedoe")

    def test_delete_details(self):
        self.client.post('/delete_details',data={"user_name":"janedoe","resource_id":1212})
        self.assert_template_used('details.html')
        self.assert_context("result", "Access is not allowed")
        self.assert_context("username", "janedoe")

    def test_logout(self):
        self.client.post('/logout',data={"user_name":"janedoe"})
        self.assert_template_used('login.html')