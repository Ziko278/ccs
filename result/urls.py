from django.urls import path
from result.views import *

urlpatterns = [

    path('result/field/create', ResultFieldCreateView.as_view(), name='result_field_create'),
    path('result/field/index', ResultFieldListView.as_view(), name='result_field_index'),
    path('result/field/<int:pk>/edit', ResultFieldUpdateView.as_view(), name='result_field_edit'),
    path('result/field/<int:pk>/delete', ResultFieldDeleteView.as_view(), name='result_field_delete'),


    path('result/grade/create', ResultGradeCreateView.as_view(), name='result_grade_create'),
    path('result/grade/index', ResultGradeListView.as_view(), name='result_grade_index'),
    path('result/grade/<int:pk>/edit', ResultGradeUpdateView.as_view(), name='result_grade_edit'),
    path('result/grade/<int:pk>/delete', ResultGradeDeleteView.as_view(), name='result_grade_delete'),

    path('result/mid-grade/create', MidResultGradeCreateView.as_view(), name='mid_result_grade_create'),
    path('result/mid-grade/index', MidResultGradeListView.as_view(), name='mid_result_grade_index'),
    path('result/mid-grade/<int:pk>/edit', MidResultGradeUpdateView.as_view(), name='mid_result_grade_edit'),
    path('result/mid-grade/<int:pk>/delete', MidResultGradeDeleteView.as_view(), name='mid_result_grade_delete'),


    path('result/behaviour-category/create', ResultBehaviourCategoryCreateView.as_view(),
         name='result_behaviour_category_create'),
    path('result/behaviour-category/index', ResultBehaviourCategoryListView.as_view(),
         name='result_behaviour_category_index'),
    path('result/behaviour-category/<int:pk>/edit', ResultBehaviourCategoryUpdateView.as_view(),
         name='result_behaviour_category_edit'),
    path('result/behaviour-category/<int:pk>/delete', ResultBehaviourCategoryDeleteView.as_view(),
         name='result_behaviour_category_delete'),

    path('result/behaviour/create', ResultBehaviourCreateView.as_view(),
         name='result_behaviour_create'),
    path('result/behaviour/index', ResultBehaviourListView.as_view(),
         name='result_behaviour_index'),
    path('result/behaviour/<int:pk>/edit', ResultBehaviourUpdateView.as_view(),
         name='result_behaviour_edit'),
    path('result/behaviour/<int:pk>/delete', ResultBehaviourDeleteView.as_view(),
         name='result_behaviour_delete'),

    path('pre-upload', result_create_view, name='result_create'),
    path('text-based-result/pre-upload', text_result_create_view, name='text_based_result_create'),
    path('text-based-result/<str:student_pk>/upload', text_result_upload_view, name='text_based_result_upload'),
    path('upload', result_upload_view, name='result_upload'),
    path('uploaded-results', uploaded_result, name='uploaded_result'),
    path('check', result_check_view, name='result_check'),
    path('check-archive', result_archive_check_view, name='result_archive_check'),
    path('index', result_index_view, name='result_index'),
    path('spreadsheet', result_spreadsheet_check_view, name='result_spreadsheet'),
    path('text-based-result/<str:student_pk>/index', text_result_index_view, name='text_based_result_index'),
    path('class_list', result_class_list_view, name='result_class_list'),
    path('student/<int:pk>', result_student_detail_view, name='result_student_detail'),
    path('affective_domain/<int:pk>', result_affective_domain_view, name='result_affective_domain'),
    path('student/<int:pk>/sheet', result_student_sheet_view, name='result_student_sheet'),

    path('student/<int:pk>/result-archive/sheet', result_archive_student_sheet_view, name='result_archive_sheet'),
    path('student/<int:pk>/sheet', result_student_sheet_view, name='result_student_sheet'),
    path('student/<int:student_pk>/cumulative_result/<int:session_pk>/<int:student_class>/<int:class_section>',
         result_cumulative_sheet_view,
         name='result_cumulative_sheet'),
    path('select-cumulative-result', select_result_cumulative_view, name='select_result_cumulative_view'),

    path('text-result-category/create', TextResultCategoryCreateView.as_view(),
         name='text_result_category_create'),
    path('text-result-category/index', TextResultCategoryListView.as_view(),
         name='text_result_category_index'),
    path('text-result-category/<int:pk>/edit', TextResultCategoryUpdateView.as_view(),
         name='text_result_category_edit'),
    path('text-result-category/<int:pk>/assign-teachers', TextResultCategoryTeacherView.as_view(),
         name='text_result_category_teacher'),
    path('text-result-category/<int:pk>/delete', TextResultCategoryDeleteView.as_view(),
         name='text_result_category_delete'),

    path('text-result/create', TextResultCreateView.as_view(), name='text_result_create'),
    path('text-result/index', TextResultListView.as_view(), name='text_result_index'),
    path('text-result/<int:pk>/edit', TextResultUpdateView.as_view(), name='text_result_edit'),
    path('text-result/<int:pk>/delete', TextResultDeleteView.as_view(), name='text_result_delete'),

    path('teacher-comment/create', TeacherResultCommentCreateView.as_view(), name='teacher_comment_create'),
    path('teacher-comment/index', TeacherResultCommentListView.as_view(), name='teacher_comment_index'),
    path('teacher-comment/<int:pk>/edit', TeacherResultCommentUpdateView.as_view(), name='teacher_comment_edit'),
    path('teacher-comment/<int:pk>/delete', TeacherResultCommentDeleteView.as_view(), name='teacher_comment_delete'),

    path('head-teacher-comment/create', HeadTeacherResultCommentCreateView.as_view(),
         name='head_teacher_comment_create'),
    path('head-teacher-comment/index', HeadTeacherResultCommentListView.as_view(),
         name='head_teacher_comment_index'),
    path('head-teacher-comment/<int:pk>/edit', HeadTeacherResultCommentUpdateView.as_view(),
         name='head_teacher_comment_edit'),
    path('head-teacher-comment/<int:pk>/delete', HeadTeacherResultCommentDeleteView.as_view(),
         name='head_teacher_comment_delete'),

    path('result-info', ResultSettingView.as_view(), name='result_info'),
    path('result-info/create', ResultSettingCreateView.as_view(), name='result_info_create'),
    path('result-info/<int:pk>/update', ResultSettingUpdateView.as_view(), name='result_info_update'),

]

