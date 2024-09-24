import time
import threading
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from .models import UserProfile, Books
from django.contrib.admin.models import LogEntry, DELETION
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


'''
Question 1: By default are django signals executed synchronously or asynchronously? 
Please support your answer with a code snippet that conclusively proves your stance. 
The code does not need to be elegant and production ready, we just need to understand your logic.

Answer 1 : 
By default, Django signals are executed synchronously, meaning that they are executed in the same thread and process as the triggering event. 
This can impact performance if the signal handler takes a long time to execute, as it will block the flow of the code.

code output :
    Before Creating user...Before triggering signal!
    Signal triggered! Sending welcome email...
    This action takes 5 sec time
    Email sent to hansonstephanie@example.net
    User profile saved in the database!
'''

#Signal to send email after saving a UserProfile
@receiver(post_save, sender=UserProfile)
def send_welcome_email(sender, instance, **kwargs):
    print("Signal triggered! Sending welcome email...")
    print("This action takes 5 sec time")
    # Simulate a long-running task (e.g., sending an email)
    time.sleep(5)  # 5 seconds delay to simulate the long-running task
    print(f"Email sent to {instance.email}")
    

'''
Question 2: Do django signals run in the same thread as the caller? 
Please support your answer with a code snippet that conclusively proves your stance.
The code does not need to be elegant and production ready, we just need to understand your logic.

Answer 2 : Yes, Django signals run in the same thread as the caller by default. This means that if a signal handler is triggered, 
it executes within the same thread that emitted the signal, blocking further code execution until the signal handler completes.

code output :
    View is running in thread: Thread-1 (ID: 14752)
    Signal triggered!
    Signal is running in thread: Thread-1 (ID: 14752)
    Book saved in the database!
'''

#Using Django Signal to Log Thread Information
@receiver(post_save, sender=Books)
def log_thread_info(sender, instance, **kwargs):
    print("Signal triggered!")
    current_thread = threading.current_thread()
    print(f"Signal is running in thread: {current_thread.name} (ID: {current_thread.ident})")
    
    
'''
Question 3: By default do django signals run in the same database transaction as the caller? 
Please support your answer with a code snippet that conclusively proves your stance. 
The code does not need to be elegant and production ready, we just need to understand your logic.

Answer 3 : Yes, by default, Django signals run in the same database transaction as the caller. 
This means that if the transaction in the calling code is rolled back, 
the changes made by the signal will also be rolled back. Similarly, 
if the transaction commits, the changes made by the signal will be committed.

code output :
    User created with ID: 7
    Signal triggered! Deleting user ...
    User Id :  7
    Log delete entry created! for  :  thomashuffman
    User deleted from the database!
    Log entries in database for this user before roll back : 1
    Exception caught: Simulated error! Rolling back the transaction.
    Log entries in database for this user after rolled back: 0
'''

#Using Django Signals and Database Transactions
    
@receiver(post_delete, sender=User)
def log_user_deletion(sender, instance, **kwargs):
    print("Signal triggered! Deleting user ...")
    print('User Id : ',instance.id)
    LogEntry.objects.create(
        user_id=instance.id,  # Use the deleted user's ID
        content_type_id=ContentType.objects.get_for_model(User).pk,
        object_id=instance.id,
        object_repr=str(instance),
        action_flag=DELETION,
        change_message="User deleted"
    )
    print("Log delete entry created! for  : ",instance.username)