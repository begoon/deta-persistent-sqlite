from django.contrib import admin


class ApplicationAdminSite(admin.AdminSite):
    site_title = 'CMS'
    site_header = site_title
    index_title = 'Configuration'
    site_url = "/"
