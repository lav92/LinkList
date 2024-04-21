from django.urls import path

from links.views import (RegistrationView, LoginView, MyAccountView, LogoutView, ChangePassword, LinkToCollection,
                         LinkCreateView, AllLinksView,SingleLinkView, UpdateLinkView, DeleteLinkView,
                         CollectionCreateView, AllCollectionView, SingleCollectionView, UpdateCollectionView,
                         DeleteCollectionView)

urlpatterns = [
    # users urls
    path("user/register/", RegistrationView.as_view(), name="register"),
    path("user/login/", LoginView.as_view(), name="login"),
    path("user/account/", MyAccountView.as_view(), name="account"),
    path("user/logout/", LogoutView.as_view(), name="logout"),
    path("user/change_password/", ChangePassword.as_view(), name="change_password"),
    # links urls
    path("links/create/", LinkCreateView.as_view(), name="create_link"),
    path("links/all_my_links/", AllLinksView.as_view(), name="all_links"),
    path("links/single_my_link/<int:pk>/", SingleLinkView.as_view(), name="single_link"),
    path("links/update_link/<int:pk>/", UpdateLinkView.as_view(), name="update_link"),
    path("links/delete/<int:pk>/", DeleteLinkView.as_view(), name="delete_link"),
    path("links/add_to_collection/", LinkToCollection.as_view(), name="link_to_collection"),
    # collections urls
    path("collections/create/", CollectionCreateView.as_view(), name="collection_create"),
    path("collections/all_my_collections/", AllCollectionView.as_view(), name="all_collections"),
    path("collections/single_my_collection/<int:pk>/", SingleCollectionView.as_view(), name="single_collection"),
    path("collections/update/<int:pk>/", UpdateCollectionView.as_view(), name="update_collection"),
    path("collections/delete/<int:pk>/", DeleteCollectionView.as_view(), name="delete_collection"),
]
