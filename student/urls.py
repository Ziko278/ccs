from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from student.views import *


urlpatterns = [
    path('student/<int:parent_pk>/register', StudentCreateView.as_view(), name='student_create'),
    path('student/index', StudentListView.as_view(), name='student_index'),
    path('student/class/index', class_student_list_view, name='student_class_index'),
    path('student/alumni/index', StudentAlumniListView.as_view(), name='student_alumni_index'),
    path('<int:pk>/detail', StudentDetailView.as_view(), name='student_detail'),
    path('<int:pk>/edit', StudentUpdateView.as_view(), name='student_edit'),
    path('<int:pk>/disable', disable_student_view, name='student_disable'),
    path('student-login-detail', student_login_detail_view, name='student_login_detail'),
    path('<int:pk>/delete', StudentDeleteView.as_view(), name='student_delete'),

    path('student/check_parent', student_check_parent_view, name='student_check_parent'),
    path('parent/register', ParentCreateView.as_view(), name='parent_create'),
    path('student-registration/parent/register', ParentCreateView.as_view(), name='student_parent_create'),
    path('parent/index', ParentListView.as_view(), name='parent_index'),
    path('parent/<int:pk>/detail', ParentDetailView.as_view(), name='parent_detail'),
    path('parent/<int:pk>/edit', ParentUpdateView.as_view(), name='parent_edit'),
    path('parent/<int:pk>/delete', ParentDeleteView.as_view(), name='parent_delete'),

    path('student-info', StudentSettingView.as_view(), name='student_info'),
    path('student-info/create', StudentSettingCreateView.as_view(), name='student_info_create'),
    path('student-info/<int:pk>/update', StudentSettingUpdateView.as_view(), name='student_info_update'),

 path(
        'paste-create-parents/',
        paste_create_parents_view,
        name='paste_create_parents'
    ),

    # The URL that the JavaScript will call to create each parent (the AJAX endpoint)
    path(
        'ajax/create-parent/',
        ajax_create_parent_view,
        name='ajax_create_parent'
    ),

path(
        'paste-create-students/',
        paste_create_students_view,
        name='paste_create_students'
    ),
    path(
        'ajax/create-student/',
        ajax_create_student_view,
        name='ajax_create_student'
    ),
]
