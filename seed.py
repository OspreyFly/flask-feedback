from app import app, db, User, Feedback

# Use the application context
with app.app_context():
    db.drop_all()
    db.create_all()

    # Define new instances of User
    user1 = User(
        username="john_doe",
        password="password123",
        email="john.doe@example.com",
        first_name="John",
        last_name="Doe",
    )

    user2 = User(
        username="jane_doe",
        password="pass456",
        email="jane.doe@example.com",
        first_name="Jane",
        last_name="Doe",
    )

    user3 = User(
        username="bob_smith",
        password="bobpass",
        email="bob.smith@example.com",
        first_name="Bob",
        last_name="Smith",
    )

    for user in [user1, user2, user3]:
        user.set_password(user.password)

    # Add the instances to the session and commit
    db.session.add_all([user1, user2, user3])
    db.session.commit()
