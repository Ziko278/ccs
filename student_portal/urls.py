from django.urls import path
from student_portal.views import *


urlpatterns = [
    path('my-classmate', StudentClassMateView.as_view(), name='student_classmate'),

    path('fee/dashboard', StudentFeeDashboardView.as_view(), name='student_fee_dashboard'),

    path('account-details/', AccountDetailView.as_view(), name='parent_account_detail'),
    path('fees/', FeeInvoiceListView.as_view(), name='parent_fee_list'),
    path('fees/invoice/<int:pk>/', FeeInvoiceDetailView.as_view(), name='parent_fee_invoice_detail'),
    # Added detail view
    path('fees/upload/', FeeUploadView.as_view(), name='parent_fee_upload'),
    path('fees/history/', FeeUploadHistoryView.as_view(), name='parent_fee_history'),

    path('dashboard', StudentDashboardView.as_view(), name='student_dashboard'),
    path('result/<int:pk>/current-result', current_term_result, name='student_current_result'),
    path('result-select', ResultSelectView.as_view(), name='student_result_select'),
    path('result/<int:pk>/result-archive/sheet', student_result_archive_sheet_view, name='student_result_archive_sheet'),

    path('lesson-note/index', StudentLessonNoteListView.as_view(), name='student_lesson_note_index'),
    path('lesson-note/<int:pk>/detail', StudentLessonNoteDetailView.as_view(), name='student_lesson_note_detail'),

]

