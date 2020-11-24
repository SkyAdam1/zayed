from django import forms

from .models import (Application, ApplicationComment, ApplicationRemark,
                     ApplicationReport, DesignatedExpert)


class ApplicationCreateForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = (
            'project_name', 'project_site', 'data_project_start', 'legal_entity',
            'project_stage', 'project_description', 'businessmodel_description', 'problem_decision',
            'consumer_decision', 'product_difference', 'have_photo', 'photo_video_project', 'patentability',
            'market_size', 'marketing_description', 'sale_strategy', 'desciption_risk', 'client_count',
            'previous_investors', 'middle_cost', 'budget_development', 'middle_revenue', 'team_count',
            'fio_team', 'team_education', 'team_experience', 'position_member', 'team_create', 'ready_relocate',
            'ready_development', 'adress_company', 'inn_company', 'fio', 'email', 'upload')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class DesignatedExpertForm(forms.ModelForm):
    class Meta:
        model = DesignatedExpert
        fields = ('expert', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class ApplicationCommentForm(forms.ModelForm):
    class Meta:
        model = ApplicationComment
        fields = ('text', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class ApplicationReportForm(forms.ModelForm):
    class Meta:
        model = ApplicationReport
        fields = ['app', 'upload' , 'year' , 'quarter' ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class ApplicationRemarkForm(forms.ModelForm):
    class Meta:
        model = ApplicationRemark
        fields = ('text', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
