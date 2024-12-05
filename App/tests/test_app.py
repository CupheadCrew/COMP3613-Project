import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from unittest.mock import MagicMock, patch
from App.models import User, Admin, Alumni, Company, Listing, Application, Employee
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user,
    add_admin,
    add_alumni,
    add_company,
    add_listing,
    subscribe,
    unsubscribe,
    add_categories,
    apply_listing,
    get_all_applicants,
    get_alumni,
    add_employee, 
    get_all_employees, 
    get_all_employees_json, 
    get_employee,
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    # def test_new_user(self):
    #     user = User("bob", "bobpass")
    #     assert user.username == "bob"

    def test_new_admin(self):
        admin = Admin('bob', 'bobpass', 'bob@mail')
        assert admin.username == "bob"

    def test_new_alumni(self):
        alumni = Alumni('rob', 'robpass', 'rob@mail', '123456789', '1868-333-4444', 'robfname', 'roblname')
        assert alumni.username == 'rob'
    
    def test_new_company(self):
        company = Company('company1', 'company1', 'compass', 'company@mail',  'company_address', 'contact', 'company_website.com')
        assert company.company_name == 'company1'

    def test_new_employee(self):
        employee = Employee('hob', 'hobpass', 'hob@mail', '234567890', 'hobfname', 'hoblname', 'Accounting')
        assert employee.username == 'hob'

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = Admin("bob", "bobpass", 'bob@mail')
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob", 'email':'bob@mail'})

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = Admin("bob", "bobpass", 'bob@mail')
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob", 'email':'bob@mail'})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = Admin("bob", password, 'bob@mail')
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = Admin("bob", password, 'bob@mail')
        assert user.check_password(password)

class EmployeeControllerTest(unittest.TestCase):

    @patch("App.controllers.db.session")  # Mock the database session
    @patch("App.controllers.Alumni.query")
    @patch("App.controllers.Admin.query")
    @patch("App.controllers.Employee")
    def test_add_employee_success(self, MockEmployee, MockAdminQuery, MockAlumniQuery, MockDBSession):
        MockAlumniQuery.filter_by().first.return_value = None
        MockAdminQuery.filter_by().first.return_value = None
        new_employee = MockEmployee.return_value

        result = add_employee("john_doe", "securepassword", "john@example.com", "EMP001", "John", "Doe", "HR")

        MockEmployee.assert_called_once_with("john_doe", "securepassword", "john@example.com", "EMP001", "John", "Doe", "HR")
        MockDBSession.add.assert_called_once_with(new_employee)
        MockDBSession.commit.assert_called_once()
        self.assertEqual(result, new_employee)

    @patch("App.controllers.db.session")
    @patch("App.controllers.Alumni.query")
    @patch("App.controllers.Admin.query")
    def test_add_employee_duplicate_username_or_email(self, MockAdminQuery, MockAlumniQuery, MockDBSession):
        MockAlumniQuery.filter_by().first.return_value = MagicMock()  # Simulate duplicate username/email

        result = add_employee("duplicate_user", "securepassword", "dup@example.com", "EMP002", "Jane", "Doe", "Finance")

        self.assertIsNone(result)
        MockDBSession.add.assert_not_called()
        MockDBSession.commit.assert_not_called()

    @patch("App.controllers.db.session")
    def test_add_employee_database_error(self, MockDBSession):
        MockDBSession.add.side_effect = Exception  # Simulate a database error

        result = add_employee("error_user", "securepassword", "error@example.com", "EMP003", "Alice", "Smith", "IT")

        self.assertIsNone(result)
        MockDBSession.rollback.assert_called_once()

    @patch("App.controllers.db.session")
    @patch("App.controllers.Employee.query")
    def test_get_all_employees(self, MockEmployeeQuery, MockDBSession):
        mock_employees = [MagicMock(), MagicMock()]
        MockEmployeeQuery.all.return_value = mock_employees

        result = get_all_employees()

        MockEmployeeQuery.all.assert_called_once()
        self.assertEqual(result, mock_employees)

    @patch("App.controllers.get_all_employees")
    def test_get_all_employees_json(self, MockGetAllEmployees):
        mock_employee_1 = MagicMock()
        mock_employee_1.get_json.return_value = {"id": 1, "name": "John"}
        mock_employee_2 = MagicMock()
        mock_employee_2.get_json.return_value = {"id": 2, "name": "Jane"}
        MockGetAllEmployees.return_value = [mock_employee_1, mock_employee_2]

        result = get_all_employees_json()

        self.assertEqual(result, [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}])

    @patch("App.controllers.Employee.query")
    def test_get_employee(self, MockEmployeeQuery):
        mock_employee = MagicMock()
        MockEmployeeQuery.filter_by().first.return_value = mock_employee

        result = get_employee("EMP001")

        MockEmployeeQuery.filter_by.assert_called_once_with(employee_id="EMP001")
        self.assertEqual(result, mock_employee)


class TestApplyToListing(unittest.TestCase):
    @patch('App.models.Application.query.filter_by')
    @patch('App.models.Listing.query.get')
    @patch('App.models.Alumni.query.filter_by')
    @patch('App.models.db.session.add')
    @patch('App.models.db.session.commit')
    @patch('App.models.Listing.notify_company_of_application')
    def test_apply_to_listing(self, mock_notify, mock_commit, mock_db_add, mock_alumni_query, mock_listing_query, mock_application_query):
        alumni_id = 123
        listing_id = 1
        alumni_name = "John Doe"
        
        # Creating mock alumni and listing objects
        mock_alumni = MagicMock(spec=Alumni)
        mock_alumni.alumni_id = alumni_id
        mock_alumni.alumni_name = alumni_name
        
        mock_listing = MagicMock(spec=Listing)
        mock_listing.id = listing_id
        
        # Mocking the query results
        mock_listing_query.return_value = mock_listing
        mock_alumni_query.return_value.filter_by.return_value.first.return_value = mock_alumni
        
        # Create a mock application instance
        mock_application = MagicMock(spec=Application)
        
        # Mock the db add operation
        mock_db_add.return_value = None

        # Call the function under test
        result = apply_to_listing()
        
        # Assert the application was created
        mock_db_add.assert_called_once_with(mock_application)
        mock_commit.assert_called_once()
        
        # Ensure the notify_company_of_application method was called
        mock_notify.assert_called_once_with(alumni_name)
        
        # Check that the response is as expected
        self.assertEqual(result[0], 200)
        self.assertEqual(result[1]["message"], "Application submitted successfully!")

    @patch('App.models.Application.query.filter_by')
    @patch('App.models.Listing.query.get')
    @patch('App.models.Alumni.query.filter_by')
    def test_alumni_or_listing_not_found(self, mock_alumni_query, mock_listing_query, mock_application_query):
        alumni_id = 123
        listing_id = 1
        
        # Mock queries to return None for either alumni or listing
        mock_listing_query.return_value = None  # Listing not found
        mock_alumni_query.return_value.filter_by.return_value.first.return_value = MagicMock(spec=Alumni)

        result = apply_to_listing()

        # Assert error message when listing is not found
        self.assertEqual(result[0], 404)
        self.assertEqual(result[1]["message"], "Alumni or Listing not found!")


'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = add_admin("bob", "bobpass", 'bob@mail')
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_admin(self):
        add_admin("bob", "bobpass", 'bob@mail')
        admin = add_admin("rick", "bobpass", 'rick@mail')
        assert admin.username == "rick"

    def test_create_alumni(self):
        alumni = add_alumni('rob', 'robpass', 'rob@mail', '123456789', '1868-333-4444', 'robfname', 'roblname')
        assert alumni.username == 'rob'

    def test_create_company(self):
        company = add_company('company1', 'company1', 'compass', 'company@mail',  'company_address', 'contact', 'company_website.com')
        assert company.username == 'company1' and company.company_name == 'company1'

    # cz at the beginning so that it runs after create company
    def test_czadd_listing(self):
        listing = add_listing('listing1', 'listing1 description', 'company1', '8000', 'Full-time', True, True, 'desiredcandidate', 'curepe')
        assert listing.title == 'listing1' and listing.company_name == 'company1'

    def test_czsubscribe(self):

        alumni = subscribe('123456789', 'Database Manager')
        assert alumni.subscribed == True

    # def test_czadd_categories(self):

    #     alumni = add_categories('123456789', ['Database'])

    #     assert alumni.get_categories() == ['Database']

    def test_czapply_listing(self):

        alumni = apply_listing('123456789', 1)

        assert get_all_applicants('1')  == [get_alumni('123456789')]


    # def get_all_applicants(self):

    #     applicants = get_all_applicants('1')

    

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([
            {"id":1, "username":"bob", 'email':'bob@mail'},
            {"id":2, "username":"rick", 'email':'rick@mail'},
            {"id":1, "username":"rob", "email":"rob@mail", "alumni_id":123456789, "subscribed":True, "job_category":'Database Manager', 'contact':'1868-333-4444', 'firstname':'robfname', 'lastname':'roblname'},
            {"id":1, "company_name":"company1", "email":"company@mail", 'company_address':'company_address','contact':'contact',
            'company_website':'company_website.com'}
            ], users_json)

    # def test_create_user(self):
    #     user = create_user("rick", "bobpass")
    #     assert user.username == "rick"

    # def test_get_all_users_json(self):
    #     users_json = get_all_users_json()
    #     self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # # Tests data changes in the database
    # def test_update_user(self):
    #     update_user(1, "ronnie")
    #     user = get_user(1)
    #     assert user.username == "ronnie"
        

