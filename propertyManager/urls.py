from django.urls import path
from .views import PropertyPostListView, ProperyPostView,PropertyUpdateApiView, get_properties_for_current_user,PropertyImportExportview,propertyexportview,PropertyDeleteApiView,PropertyUpdateImageApiView,imageaddApiview
urlpatterns = [
    path('list/', PropertyPostListView.as_view(), name="propertyList"),
    path('list/<int:pk>', PropertyPostListView.as_view(), name="property"),

    path('post_property/', ProperyPostView.as_view(), name="post_property"),
    path("user_property/", get_properties_for_current_user, name="usersProperty"),
    path("delete_property/<int:pk>", PropertyDeleteApiView.as_view(), name="property_delete"),
    path("update_property/<int:pk>", PropertyUpdateApiView.as_view(), name="property_update"),
    path("getexcel/",PropertyImportExportview.as_view(),name="exporttoexcel"),
    path("uploadexcel/",propertyexportview.as_view(),name="uploadfile"),
    path("updateimage/<int:pk>",PropertyUpdateImageApiView.as_view()),
    path("addimage/<int:pk>",imageaddApiview.as_view()),
]
