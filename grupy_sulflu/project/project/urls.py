"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponse
from django.template import Context, Template


def template_view(request):
    texto = """
    <h1>Classe de template: {{ template_class }}</h1>
    <h1>Classe de Contexto: {{ context_class }}</h1>
    """

    template = Template(texto)
    contexto = {
        "template_class": str(Template),
        "context_class": str(Context)
    }
    return HttpResponse(
        template.render(Context(contexto))
    )

def olar(request):
    return HttpResponse('<h1>Olar!</h1>')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', olar),
    url(r'^templates/$', template_view),
    url(r'^cinema/', include('cinema.urls')),
]

