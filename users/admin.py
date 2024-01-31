from django.contrib import admin

from users.models import User, Skils, Portfolio, PortfolioPhoto

admin.site.register(User)
admin.site.register(Skils)
admin.site.register(Portfolio)
admin.site.register(PortfolioPhoto)
