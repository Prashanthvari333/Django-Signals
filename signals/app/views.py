from django.shortcuts import render

from django.http import HttpResponse

from .models import UserProfile , Books
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry, DELETION
from django.contrib.contenttypes.models import ContentType

import threading
from django.db import transaction
from faker import Faker

# Create your views here.


# Initialize Faker instance
fake = Faker()





def  index(request):
    return HttpResponse("<H1> Hello , You can explore signals now..!</H1>")


def create_user_profile(request):
    print('Before Creating user...Before triggering signal!')
    # Generate fake data
    username = fake.user_name()
    email = fake.email()
    
    # Simulate user profile creation
    profile = UserProfile.objects.create(user=username, email=email)
    print("User profile saved in the database!") # this line will execute after time taken signal
    # Pass the profile data to the template
    context = {
        'name': profile.user,
        'email': profile.email,
    }
    return render(request, 'profile.html', context)

def create_book(request):
    # Log the current thread in the view
    current_thread = threading.current_thread()
    print(f"View is running in thread: {current_thread.name} (ID: {current_thread.ident})")
    
    # Generate fake data
    book_title = fake.sentence(nb_words=3)  # Generating a book title with 3 words
    author = fake.name()
    
    # Create the Book
    Book = Books.objects.create(title=book_title, author =author)
    print("Book saved in the database!")
    
    
    context = {
        'title': Book.title,
        'author': Book.author,
    }
    return render(request, 'books.html', context)




def delete_user(request):
    
    # Generate fake data
    username = fake.user_name()
    email = fake.email()
    password = fake.password()
    # First, ensure we have a user and profile to delete
    user = User.objects.create_user(username=username, email=email, password=password)
    user_id = user.id
    print(f"User created with ID: {user_id}")

    try:
        with transaction.atomic():
            # Delete the User instance
            user = User.objects.get(id=user_id)
            user.delete()
            print("User deleted from the database!")
            
            # Check  LogEntry before rolled back 
            logs = LogEntry.objects.filter(object_id=str(user_id), content_type=ContentType.objects.get_for_model(User))
            print(f"Log entries in database for this user before roll back : {logs.count()}")


            # Simulate an error after signal is triggered
            raise Exception("Simulated error! Rolling back the transaction.")
    except Exception as e:
        print(f"Exception caught: {e}")

    # Check if LogEntry was rolled back and if the profile and user still exist
    logs = LogEntry.objects.filter(object_id=str(user_id), content_type=ContentType.objects.get_for_model(User))
    print(f"Log entries in database for this user after rolled back: {logs.count()}")
    
    try:
        user = User.objects.get(id=user_id)
        user_exists = True
    except (User.DoesNotExist, UserProfile.DoesNotExist):
        user_exists = False

    # Prepare context for the template
    context = {
        'user_id': user_id,
        'user_exists': user_exists,
        'log_count': logs.count(),
    }
    return render(request, 'user_deletion.html', context)

