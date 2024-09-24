# Django Signals Example
This repository demonstrates the default behavior of Django signals, including their synchronous execution, running in the same thread as the caller, and participation in the same database transaction as the caller. The project is built using Django with examples that cover:

- Synchronous execution of signals
- Signals running in the same thread
- Signals and database transactions
# Prerequisites
Before you get started, ensure you have the following installed:

- Python 3.x
- Django 4.x
- A database (e.g., SQLite, PostgreSQL)
  
# Debugging Signals
To better understand how signals work, follow the steps below to trigger different signal-related actions and observe the output.

## Scenario 1: Synchronous Signal Execution
Visit the create_user_profile view at /create-user-profile/.

Check the console logs to observe how the signal triggers after saving the UserProfile object and blocks the flow for 5 seconds.

Output:
```bash
Before Creating user...Before triggering signal!
Signal triggered! Sending welcome email...
This action takes 5 sec time
Email sent to example@example.com
User profile saved in the database!
```
## Scenario 2: Signals Running in the Same Thread
Visit the create_book view at /create-book/.

Check the console logs to see the thread information for both the view and the signal.

Output:
```bash
View is running in thread: Thread-1 (ID: 14752)
Signal triggered!
Signal is running in thread: Thread-1 (ID: 14752)
Book saved in the database!
```

## Scenario 3: Signals and Database Transactions
Visit the delete_user view at /delete-user/.

Observe how the signal creates a log entry when a user is deleted.

Simulate an error to roll back the transaction and see that both the user deletion and the log entry are rolled back.

Output:
```bash
User created with ID: 7
Signal triggered! Deleting user ...
User Id :  7
Log delete entry created! for  : user123
User deleted from the database!
Log entries in database for this user before roll back : 1
Exception caught: Simulated error! Rolling back the transaction.
Log entries in database for this user after rolled back: 0
```

# Example Scenarios
The following views are used to demonstrate the behavior of Django signals:

Create User Profile: Triggers a signal when a UserProfile object is created.
  - URL: /create-user-profile/
Create Book: Triggers a signal and logs thread information when a Books object is created.
  - URL: /create-book/
Delete User: Simulates a user deletion, logs the deletion using signals, and rolls back the transaction.
  - URL: /delete-user/
