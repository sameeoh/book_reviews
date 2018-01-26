from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect

from django.contrib import messages

from .models import *

import bcrypt

# LOGIN AND REGISTRATION
def index(request):
    if not 'status' in request.session:
        request.session['status'] = 'test'
    if 'user_id' in request.session:
        return redirect('/home')
    return render(request, 'reviews/index.html')

def home(request):
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    reviews = Review.objects.all().order_by('-created_at')[:3]
    books = Book.objects.all()
    context = {
        'user': user,
        'status': request.session['status'],
        'reviews': reviews,
        'books': books,
    }
    return render(request, 'reviews/home.html', context)

def register(request):
    errors = []
    if len(request.POST['name']) < 1:
        errors.append("Name must be at least two characters.")
    if len(request.POST['alias']) < 1:
        errors.append("Alias must be at least two characters.")
    if len(request.POST['email']) < 3:
        errors.append("Email must be at least four characters.")
    if len(request.POST['password']) < 7:
        errors.append("Password must be at least eight characters.")
    if request.POST['password'] != request.POST['password_confirmation']:
        errors.append("Password and password confirmation don't match.")
    if errors:
        for err in errors:
            messages.error(request, err)

        return redirect('/')
    else:
        try:
            User.objects.get(email=request.POST['email'])
            messages.error(request, "User with that email already exists.")
            return redirect('/')
        except User.DoesNotExist:
            hashpw = bcrypt.hashpw(
                request.POST['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(
                name=request.POST['name'], alias=request.POST['alias'], password=hashpw, email=request.POST['email'])
            request.session['user_id'] = user.id
            request.session['status'] = 'Registered'
            return redirect('/home')

def login(request):
    try:
        user = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user_id'] = user.id
            request.session['status'] = 'Logged In'
            return redirect('/home')
        else:
            messages.error(request, "Email/Password combination FAILED")
            return redirect('/')
    except User.DoesNotExist:
        messages.error(request, "Email does not exist. Please try again")
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

# BOOK REVIEWS

def add(request):
    authors = Author.objects.all()
    context = {
        'authors': authors,
    }
    return render(request, 'reviews/add.html', context)

def add_book(request):
    title = request.POST['title']
    review = request.POST['review']
    rating = request.POST['rating']

    if len(request.POST['newauthor']) == 0:
        author = Author.objects.get(id=request.POST['author'])
    else:
        try:
            Author.objects.get(name=request.POST['newauthor'])
            messages.error(request, "Author with that name already exists. Please use drop down box")
            print '@@@@@@@@@@@@@@@@@@@@@'
            print 'error occured'
            print '@@@@@@@@@@@@@@@@@@@@@'
            return redirect('/books/add')
        except:
            author = Author.objects.create(name=request.POST['newauthor'])
            print '@@@@@@@@@@@@@@@@@@@@@'
            print 'error did not occur'
            print '@@@@@@@@@@@@@@@@@@@@@'

    book = Book.objects.create(title = title, author = author)
    user = User.objects.get(id = request.session['user_id'])
    Review.objects.create(review=review, rating=rating, reviewer=user, book=book)
    
    return redirect('/books/{}'.format(book.id))

def add_review(request, id):
    review = request.POST['review']
    rating = request.POST['rating']
    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.get(id=id)
    Review.objects.create(review=review, rating=rating,
    reviewer=user, book=book)
    return redirect('/books/{}'.format(book.id))

def show_book(request, id):
    book = Book.objects.get(id=id)
    reviews = Review.objects.filter(book=book)
    context = {
        'current_book': book,
        'book_reviews': reviews,
    }
    return render(request, 'reviews/show_book.html', context)

def delete(request, id):
    review = Review.objects.get(id=id)
    bid = review.book.id
    review.delete()
    return redirect('/books/{}'.format(bid))

def reviewer(request, id):
    reviewer = User.objects.get(id=id)
    reviews = Review.objects.filter(reviewer=reviewer)
    count = reviews.count()
    context = {
        'reviewer': reviewer,
        'reviews': reviews,
        'count': count,
    }
    return render(request, 'reviews/reviewer.html', context)
