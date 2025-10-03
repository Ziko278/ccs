from django.urls import path
from finance.views import *

urlpatterns = [

    path('fee/create', FeeCreateView.as_view(), name='fee_create'),
    path('fee/index', FeeListView.as_view(), name='fee_index'),
    path('fee/<int:pk>/detail', FeeDetailView.as_view(), name='fee_detail'),
    path('fee/<int:pk>/edit', FeeUpdateView.as_view(), name='fee_edit'),
    path('fee/<int:pk>/delete', FeeDeleteView.as_view(), name='fee_delete'),

    path('fee-group/create', FeeGroupCreateView.as_view(), name='fee_group_create'),
    path('fee-group/index', FeeGroupListView.as_view(), name='fee_group_index'),
    path('fee-group/<int:pk>/detail', FeeGroupDetailView.as_view(), name='fee_group_detail'),
    path('fee-group/<int:pk>/edit', FeeGroupUpdateView.as_view(), name='fee_group_edit'),
    path('fee-group/<int:pk>/delete', FeeGroupDeleteView.as_view(), name='fee_group_delete'),

    path('fee-master/create', FeeMasterCreateView.as_view(), name='fee_master_create'),
    path('fee-master/index', FeeMasterListView.as_view(), name='fee_master_index'),
    path('fee-master/<int:pk>/detail', FeeMasterDetailView.as_view(), name='fee_master_detail'),
    path('fee-master/<int:pk>/edit', FeeMasterUpdateView.as_view(), name='fee_master_edit'),
    path('fee-master/<int:pk>/delete', FeeMasterDeleteView.as_view(), name='fee_master_delete'),

    path('fee-discount/create', FeeDiscountCreateView.as_view(), name='fee_discount_create'),
    path('fee-discount/index', FeeDiscountListView.as_view(), name='fee_discount_index'),
    path('fee-discount/<int:pk>/detail', FeeDiscountDetailView.as_view(), name='fee_discount_detail'),
    path('fee-discount/<int:pk>/edit', FeeDiscountUpdateView.as_view(), name='fee_discount_edit'),
    path('fee-discount/<int:pk>/delete', FeeDiscountDeleteView.as_view(), name='fee_discount_delete'),

    path('fee-discount-group/create', FeeDiscountGroupCreateView.as_view(), name='fee_discount_group_create'),
    path('fee-discount-group/index', FeeDiscountGroupListView.as_view(), name='fee_discount_group_index'),
    path('fee-discount-group/<int:pk>/detail', FeeDiscountGroupDetailView.as_view(), name='fee_discount_group_detail'),
    path('fee-discount-group/<int:pk>/edit', FeeDiscountGroupUpdateView.as_view(), name='fee_discount_group_edit'),
    path('fee-discount-group/<int:discount_pk>/<int:student_pk>/assign_benefactor', discount_add_benefactor_view,
         name='fee_discount_group_add_benefactor'),
    path('fee-discount-group/<int:discount_pk>/<int:student_pk>/remove_benefactor', discount_remove_benefactor_view,
         name='fee_discount_group_remove_benefactor'),

    path('fee-discount-group/<int:pk>/delete', FeeDiscountGroupDeleteView.as_view(), name='fee_discount_group_delete'),

    path('fee-penalty/create', FeePenaltyCreateView.as_view(), name='fee_penalty_create'),
    path('fee-penalty/index', FeePenaltyListView.as_view(), name='fee_penalty_index'),
    path('fee-penalty/<int:pk>/detail', FeePenaltyDetailView.as_view(), name='fee_penalty_detail'),
    path('fee-penalty/<int:pk>/edit', FeePenaltyUpdateView.as_view(), name='fee_penalty_edit'),
    path('fee-penalty/<int:pk>/delete', FeePenaltyDeleteView.as_view(), name='fee_penalty_delete'),

    path('fee/payment/select-student', FeePaymentSelectStudentView.as_view(), name='fee_select_student'),
    path('fee/payment/get-class-student', fee_get_class_students, name='fee_get_class_students'),
    path('fee/payment/get-student-by-reg-number', fee_get_class_students_by_reg_number,
         name='fee_get_class_students_by_reg_number'),

    path('fee/payment/<int:student_pk>/create', FeePaymentCreateView.as_view(), name='fee_payment_create'),
    path('fee/payment/<int:payment_pk>/<int:student_pk>/create', create_fee__payment_summary,
         name='fee_payment_summary_create'),
    path('fee/bulk-payment/create', bulk_payment_create_view, name='bulk_fee_payment_create'),
    path('fee/payment/index', fee_payment_list_view, name='fee_payment_index'),
    path('fee/payment/<int:pk>/detail', FeePaymentDetailView.as_view(), name='fee_payment_detail'),

    path('fee/payment/<int:pk>/confirm', confirm_fee_payment_view, name='fee_payment_confirm'),
    path('fee/bulk-payment/<int:pk>/confirm', confirm_bulk_fee_payment_view, name='fee_bulk_payment_confirm'),
    path('fee/payment/<int:pk>/revert', revert_fee_payment_view, name='fee_payment_revert'),
    path('fee/bulk-payment/<int:pk>/revert', revert_bulk_fee_payment_view, name='fee_bulk_payment_revert'),

    path('fee/payment/verify-paystack-payment', verfiy_paystack_payment, name='verify_paystack_payment'),
    path('fee/payment/verify-flutterwave-payment', verfiy_flutterwave_payment, name='verify_flutterwave_payment'),

    path('online-payment-method/create', OnlinePaymentCreateView.as_view(), name='online_payment_create'),
    path('online-payment-method/index', OnlinePaymentListView.as_view(), name='online_payment_index'),
    path('online-payment-method/<int:pk>/detail', OnlinePaymentDetailView.as_view(), name='online_payment_detail'),
    path('online-payment-method/<int:pk>/edit', OnlinePaymentUpdateView.as_view(), name='online_payment_edit'),
    path('online-payment-method/<int:pk>/delete', OnlinePaymentDeleteView.as_view(), name='online_payment_delete'),

    path('income-category/create', IncomeCategoryCreateView.as_view(), name='income_category_create'),
    path('income-category/index', IncomeCategoryListView.as_view(), name='income_category_index'),
    path('income-category/<int:pk>/edit', IncomeCategoryUpdateView.as_view(), name='income_category_edit'),
    path('income-category/<int:pk>/delete', IncomeCategoryDeleteView.as_view(), name='income_category_delete'),

    path('income-source/create', IncomeSourceCreateView.as_view(), name='income_source_create'),
    path('income-source/index', IncomeSourceListView.as_view(), name='income_source_index'),
    path('income-source/<int:pk>/edit', IncomeSourceUpdateView.as_view(), name='income_source_edit'),
    path('income-source/<int:pk>/delete', IncomeSourceDeleteView.as_view(), name='income_source_delete'),

    path('income/create', IncomeCreateView.as_view(), name='income_create'),
    path('income/index', IncomeListView.as_view(), name='income_index'),
    path('income/<int:pk>/detail', IncomeDetailView.as_view(), name='income_detail'),
    path('income/<int:pk>/edit', IncomeUpdateView.as_view(), name='income_edit'),
    path('income/<int:pk>/delete', IncomeDeleteView.as_view(), name='income_delete'),

    path('expense-category/create', ExpenseCategoryCreateView.as_view(), name='expense_category_create'),
    path('expense-category/index', ExpenseCategoryListView.as_view(), name='expense_category_index'),
    path('expense-category/<int:pk>/edit', ExpenseCategoryUpdateView.as_view(), name='expense_category_edit'),
    path('expense-category/<int:pk>/delete', ExpenseCategoryDeleteView.as_view(), name='expense_category_delete'),

    path('expense-type/create', ExpenseTypeCreateView.as_view(), name='expense_type_create'),
    path('expense-type/index', ExpenseTypeListView.as_view(), name='expense_type_index'),
    path('expense-type/<int:pk>/edit', ExpenseTypeUpdateView.as_view(), name='expense_type_edit'),
    path('expense-type/<int:pk>/delete', ExpenseTypeDeleteView.as_view(), name='expense_type_delete'),

    path('expense/create', ExpenseCreateView.as_view(), name='expense_create'),
    path('expense/index', ExpenseListView.as_view(), name='expense_index'),
    path('expense/<int:pk>/detail', ExpenseDetailView.as_view(), name='expense_detail'),
    path('expense/<int:pk>/edit', ExpenseUpdateView.as_view(), name='expense_edit'),
    path('expense/<int:pk>/delete', ExpenseDeleteView.as_view(), name='expense_delete'),

    path('finance-info', FinanceSettingView.as_view(), name='finance_info'),
    path('finance-info/create', FinanceSettingCreateView.as_view(), name='finance_info_create'),
    path('finance-info/<int:pk>/update', FinanceSettingUpdateView.as_view(), name='finance_info_update'),

    path('finance-dashboard', FinanceDashboardView.as_view(), name='finance_dashboard'),
    path('fee-dashboard', FeeDashboardView.as_view(), name='fee_dashboard'),

]

