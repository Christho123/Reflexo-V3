from django.urls import path
from .views.history import histories_list, history_create, history_delete, history_update, history_detail, patient_history
from .views.document_type import document_types_list, document_type_create, document_type_delete, document_type_edit
from .views.payment_type import payment_types_list, payment_type_create, payment_type_delete, payment_type_edit
from .views.predetermined_price import predetermined_prices_list, predetermined_price_create, predetermined_price_update, predetermined_price_delete
from .views.payment_status import payment_status_list, payment_status_create, payment_status_edit, payment_status_delete
from .views.contraceptive_method import (
    contraceptive_methods_list,
    contraceptive_method_create,
    contraceptive_method_edit,
    contraceptive_method_delete,
    contraceptive_method_detail,
)

from .views.diu_type import (
    diu_type_list,
    diu_type_create,
    diu_type_edit,
    diu_type_delete,
    diu_type_detail,
)

urlpatterns = [
    # Rutas de histories
    path("histories/", histories_list, name="histories_list"),
    path("histories/create/", history_create, name="history_create"),
    path("histories/<int:pk>/", history_detail, name="history_detail"),
    path("histories/<int:pk>/edit/", history_update, name="history_update"),
    path("histories/<int:pk>/delete/", history_delete, name="history_delete"),
    path("histories/patient/<int:patient_id>/", patient_history, name="patient_history"),

    path("document_types/", document_types_list, name="document_types_list"),
    path("document_types/create/", document_type_create, name="document_type_create"),
    path("document_types/<int:pk>/edit/", document_type_edit, name="document_type_edit"),
    path("document_types/<int:pk>/delete/", document_type_delete, name="document_type_delete"),

    path("payment_types/", payment_types_list, name="payment_types_list"),
    path("payment_types/create/", payment_type_create, name="payment_type_create"),
    path('payment_types/<int:pk>/edit/', payment_type_edit, name='payment_type_edit'),
    path("payment_types/<int:pk>/delete/", payment_type_delete, name="payment_type_delete"),
    
    path("payment_status/", payment_status_list, name="payment_status_list"),
    path("payment_status/create/", payment_status_create, name="payment_status_create"),
    path('payment_status/<int:pk>/edit/', payment_status_edit, name='payment_status_edit'),
    path("payment_status/<int:pk>/delete/", payment_status_delete, name="payment_status_delete"),
    
    path("predetermined_prices/", predetermined_prices_list, name="predetermined_prices_list"),
    path("predetermined_prices/create/", predetermined_price_create, name="predetermined_price_create"),
    path("predetermined_prices/<int:pk>/edit/", predetermined_price_update, name="predetermined_price_update"),
    path("predetermined_prices/<int:pk>/delete/", predetermined_price_delete, name="predetermined_price_delete"),
    
    # Contraceptive Methods
    path("contraceptive_methods/", contraceptive_methods_list, name="contraceptive_methods_list"),
    path("contraceptive_methods/create/", contraceptive_method_create, name="contraceptive_method_create"),
    path("contraceptive_methods/<int:pk>/edit/", contraceptive_method_edit, name="contraceptive_method_edit"),
    path("contraceptive_methods/<int:pk>/delete/", contraceptive_method_delete, name="contraceptive_method_delete"),
    path("contraceptive_methods/<int:pk>/", contraceptive_method_detail, name="contraceptive_method_detail"),

    path("diu_type/", diu_type_list, name="diu_type_list"),
    path("diu_type/create/", diu_type_create, name="diu_type_create"),
    path("diu_type/<int:pk>/edit/", diu_type_edit, name="diu_type_edit"),
    path("diu_type/<int:pk>/delete/", diu_type_delete, name="diu_type_delete"),
    path("diu_type/<int:pk>/", diu_type_detail, name="diu_type_detail"),
]