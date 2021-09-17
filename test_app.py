from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class BloglyViewsTestCase(TestCase):
    """Tests for views for Blogly"""

    def setUp(self):
        """Add sample user."""

        Post.query.delete()
        User.query.delete()

        user = User(first_name="TestFirstName",
                    last_name="TestLastName",
                    image_url="https://i.natgeofe.com/n/3faa2b6a-f351-4995-8fff-36d145116882/domestic-dog_16x9.jpg"
                    )
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        post = Post(title="Seeded Title",
                    content="Seeded content",
                    user_id=self.user_id
                    )
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_redirect_to_users_followed(self):
        """Test that redirect from / works"""
        
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_show_users(self):
        """Test that /users route works """
        
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirstName', html)

    def test_add_user(self):
        """Test that user is added."""
        
        with app.test_client() as client:
            test_new_user = {
                "first-name": "TestFirstName2",
                "last-name": "TestLastName2",
                "image-url": "https://icatcare.org/app/uploads/2018/07/Thinking-of-getting-a-cat.png"
            }
            resp = client.post("/users/new",
                               data=test_new_user,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Users</h1>", html)
            self.assertIn("TestFirstName2", html)

    def test_show_user_edit_form(self):
        """Test that user edit form works"""
        
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Edit a user</h1>", html)

    def test_add_post(self):
        """Test adding a post"""

        with app.test_client() as client:
            new_post = {
                "title": "Test title",
                "content": "Post content here"
            }
            resp = client.post(f"/users/{self.user_id}/posts/new",
                               data=new_post,
                               follow_redirects=True
                               )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test title", html)

    def test_delete_post(self):
        """Test deleting a post."""

        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post_id}/delete",
                               follow_redirects=True
                               )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Seeded Title", html)
