from django.contrib.admin.apps import AdminConfig


class ApplicationAdminConfig(AdminConfig):
    default_site = 'admin.ApplicationAdminSite'
