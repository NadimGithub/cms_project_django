from django import forms
from .models import BookMaster, LibraryTransaction

class BookMasterForm(forms.ModelForm):
    class Meta:
        model = BookMaster
        fields = '__all__'

# class LibraryTransactionForm(forms.ModelForm):
#     class Meta:
#         model = LibraryTransaction
#         fields = '__all__'
 
class LibraryTransactionForm(forms.ModelForm):
    class Meta:
        model = LibraryTransaction
        fields = ['course_id', 'staff', 'student', 'year','book_id', 'issue_date', 'return_date', 'issued_to', 'status']
        widgets = {
            'staff': forms.Select(attrs={'required': False}),
            'student': forms.Select(attrs={'required': False}),
        }