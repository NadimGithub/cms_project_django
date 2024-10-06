from django import forms
from .models import ExamPaper, Result

# class ExamMasterForm(forms.ModelForm):
#     class Meta:
#         model = ExamMaster
#         # fields = '__all__'
#         exclude=['id',]

class ExamPaperForm(forms.ModelForm):
    class Meta:
        model = ExamPaper
        exclude = ['questions','status']


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['exam', 'year', 'semester', 'division', 'subject', 'course_id', 'marks']  # Include marks by default

    def __init__(self, *args, **kwargs):
        is_update = kwargs.pop('is_update', False)
        super(ResultForm, self).__init__(*args, **kwargs)

        # Exclude 'marks' field only if it's a create operation
        if not is_update:
            self.fields.pop('marks')