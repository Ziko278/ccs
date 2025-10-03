from django.urls import path
from student_portal.views import *


urlpatterns = [
    path('my-classmate', StudentClassMateView.as_view(), name='student_classmate'),

    path('fee/dashboard', StudentFeeDashboardView.as_view(), name='student_fee_dashboard'),
    path('fee/index', StudentFeeView.as_view(), name='student_fee'),
    path('fee/upload', StudentFeePaymentCreateView.as_view(), name='student_fee_create'),
    path('fee/payments', student_fee_payment_list_view, name='student_fee_payments'),
    path('fee/payments/<int:pk>/detail', StudentFeeDetailView.as_view(), name='student_fee_detail'),
    path('fee/select-method', select_fee_method, name='select_fee_method'),
    path('fee/pay-multiple-fee', student_bulk_payment_create_view, name='student_bulk_payment'),
    path('fee/payment/<int:payment_pk>/<int:student_pk>/create', student_create_fee__payment_summary,
         name='student_fee_payment_summary_create'),

    path('dashboard', StudentDashboardView.as_view(), name='student_dashboard'),
    path('result/<int:pk>/current-result', current_term_result, name='student_current_result'),
    path('result-select', ResultSelectView.as_view(), name='student_result_select'),
    path('result/<int:pk>/result-archive/sheet', student_result_archive_sheet_view, name='student_result_archive_sheet'),

    path('lesson-note/index', StudentLessonNoteListView.as_view(), name='student_lesson_note_index'),
    path('lesson-note/<int:pk>/detail', StudentLessonNoteDetailView.as_view(), name='student_lesson_note_detail'),

]

