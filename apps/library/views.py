from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import BookMaster, LibraryTransaction
from .forms import BookMasterForm, LibraryTransactionForm
from apps.course.models import CourseMaster
from apps.staff.models import StaffMaster
from apps.student.models import StudentMaster
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

def library_dash(request):
    return render(request,'dashboard.html') 

def book_list(request):
    course_id = request.GET.get('course', '')  # Updated to match the name used in the form
    search_query = request.GET.get('search', '')
    location = request.GET.get('location', '')

    books = BookMaster.objects.all()

    if course_id:
        books = books.filter(course_id=course_id)

    if location:
        books = books.filter(self_location__icontains=location)

    if search_query:
        search_filters = Q()
        search_fields = [
            'book_name', 'author', 'category', 'copies_available', 'language',
            'condition', 'isbn', 'course_id__name'
        ]
        for field in search_fields:
            search_filters |= Q(**{f"{field}__icontains": search_query})
        books = books.filter(search_filters)

    courses = CourseMaster.objects.all()
    return render(request, 'library/library_list.html', {'books': books, 'courses': courses, 'search_query': search_query})

def book_detail(request, pk):
    book = get_object_or_404(BookMaster, pk=pk)
    return render(request, 'library/library_detail.html', {'book': book})

def book_create(request):
    courses = CourseMaster.objects.all()
    
    if request.method == 'POST':
        form = BookMasterForm(request.POST, request.FILES)
        
        # Check if the ISBN already exists
        isbn = request.POST.get('isbn')
        if BookMaster.objects.filter(isbn=isbn).exists():
            messages.error(request, "ISBN already exists in the database.")
            return render(request, 'library/library.html', {'form': form, 'course': courses, 'messages': messages.get_messages(request)})
        
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully!")
            return redirect('library_list')
        else:
            print(form.errors)  # Debugging information
        
    else:
        form = BookMasterForm()

    return render(request, 'library/library.html', {'form': form, 'course': courses})

def book_update(request, pk):
    courses = CourseMaster.objects.all()
    book = get_object_or_404(BookMaster, pk=pk)
    if request.method == 'POST':
        form = BookMasterForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('library_detail', pk=book.pk)
    else:
        form = BookMasterForm(instance=book)
    return render(request, 'library/library_form.html', {'form': form,'course':courses})


# ---------------------------------------------------ajax----------------------------------------------------------------------
def fetch_books(request):
    course_id = request.GET.get('course_id')
    books = BookMaster.objects.filter(course_id=course_id).values('id', 'book_name')

    options = '<option value="" disabled selected>Select book</option>'
    for book in books:
        options += f'<option value="{book["id"]}">{book["book_name"]}</option>'
    
    return JsonResponse(options, safe=False)
# ---------------------------------------------------ajax----------------------------------------------------------------------




def transaction_list(request):
    course_id = request.GET.get('course', '')
    search_query = request.GET.get('search', '')
    selected_year = request.GET.get('year', '')

    transactions = LibraryTransaction.objects.all()

    # Filter by course
    if course_id:
        transactions = transactions.filter(course_id=course_id)

    # Filter by year
    if selected_year:
        transactions = transactions.filter(year=selected_year)

    # Search functionality
    if search_query:
        search_filters = Q()
        search_fields = [
            'id', 'status', 'year', 'issued_by', 'issued_to'
        ]
        foreign_key_fields = {
            'course_id__name': 'course',
            'student__first_name': 'student',
            'student__middle_name': 'student',
            'student__last_name': 'student',
            'staff__name': 'staff',
            'book_id__book_name': 'book',
            'book_id__isbn': 'isbn'
        }
        for field in search_fields:
            search_filters |= Q(**{f"{field}__icontains": search_query})
        for field, related_model in foreign_key_fields.items():
            search_filters |= Q(**{f"{field}__icontains": search_query})

        transactions = transactions.filter(search_filters)

    # Pagination
    paginator = Paginator(transactions, 10)  # Show 10 transactions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get all courses for the dropdown
    courses = CourseMaster.objects.all()

    return render(request, 'library/transaction_list.html', {
        'transactions': page_obj,
        'courses': courses,
        'page_obj': page_obj,
    })

def transaction_detail(request, pk):
    transaction = get_object_or_404(LibraryTransaction, pk=pk)
    return render(request, 'library/transaction_detail.html', {'transaction': transaction})

def transaction_create(request):
    courses = CourseMaster.objects.all()
    students = StudentMaster.objects.all()
    staffs = StaffMaster.objects.all()
    books = BookMaster.objects.all()

    if request.method == 'POST':
        issued_to = request.POST.get('issued_to')
        isbn = request.POST.get('isbn')  # Get the entered ISBN
        course_id = request.POST.get('course_id')  # Get the selected course ID
        book_id = request.POST.get('book_id')  # Get the selected book ID

        form = LibraryTransactionForm(request.POST)
        if not BookMaster.objects.filter(isbn=isbn, course_id_id=course_id).exists():
            messages.error(request, "The ISBN does not match the selected course.")
            return render(request, 'library/library-transaction.html', {
                'form': form,
                'course': courses,
                'Students': students,
                'staff': staffs,
                'books': books,
            })

        # Validate if the entered book and ISBN match each other
        if not BookMaster.objects.filter(id=book_id, isbn=isbn).exists():
            messages.error(request, "The selected book does not match the entered ISBN.")
            return render(request, 'library/library-transaction.html', {
                'form': form,
                'course': courses,
                'Students': students,
                'staff': staffs,
                'books': books,
            })

        if form.is_valid():
            transaction = form.save(commit=False)
            if issued_to == 'student':
                transaction.staff = None
            elif issued_to == 'staff':
                transaction.student = None

            transaction.save()
            return redirect('transaction_list')

    else:
        form = LibraryTransactionForm()

    context = {
        'form': form,
        'course': courses,
        'Students': students,
        'staff': staffs,
        'books': books,
    }
    return render(request, 'library/library-transaction.html', context)



def transaction_update(request, pk):
    transaction = get_object_or_404(LibraryTransaction, pk=pk)
    courses = CourseMaster.objects.all()
    students = StudentMaster.objects.all()
    staffs = StaffMaster.objects.all()
    books = BookMaster.objects.all()

    if request.method == 'POST':
        issued_to = request.POST.get('issued_to')
        isbn = request.POST.get('isbn')  # Get the entered ISBN
        course_id = request.POST.get('course_id')  # Get the selected course ID
        book_id = request.POST.get('book_id')  # Get the selected book ID

        form = LibraryTransactionForm(request.POST, instance=transaction)

        # Validate if ISBN matches the selected course
        if not BookMaster.objects.filter(isbn=isbn, course_id_id=course_id).exists():
            messages.error(request, "The ISBN does not match the selected course.")
            return render(request, 'library/transection_form.html', {
                'form': form,
                'transaction': transaction,
                'course': courses,
                'Students': students,
                'staff': staffs,
                'books': books,
            })

        # Validate if the entered book and ISBN match each other
        if not BookMaster.objects.filter(id=book_id, isbn=isbn).exists():
            messages.error(request, "The selected book does not match the entered ISBN.")
            return render(request, 'library/transection_form.html', {
                'form': form,
                'transaction': transaction,
                'course': courses,
                'Students': students,
                'staff': staffs,
                'books': books,
            })

        if form.is_valid():
            transaction = form.save(commit=False)
            if issued_to == 'student':
                transaction.staff = None
            elif issued_to == 'staff':
                transaction.student = None

            transaction.save()
            return redirect('transaction_list')
    else:
        form = LibraryTransactionForm(instance=transaction)

    context = {
        'form': form,
        'transaction': transaction,
        'course': courses,
        'Students': students,
        'staff': staffs,
        'books': books,
    }
    return render(request, 'library/transection_form.html', context)
