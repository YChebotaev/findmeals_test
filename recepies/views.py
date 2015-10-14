from django.views.generic import TemplateView, FormView
from django import forms
from django.http import HttpResponse
from recepies.models import Base, Recepie, Ingredient
import json

from test_task.db_config import engine, Session

session = Session()

Base.metadata.create_all(engine)

class FindRecepieForm(forms.Form):
    query = forms.TextInput()

class IndexView(TemplateView):
    template_name = 'index.html'

def find_recepie(request):
    search = request.GET.get('query', '')

    query = session.query(Recepie)
    query = query.filter(Recepie.display_name.contains(search))

    result = [r.toJSON() for r in query]

    body = json.dumps({
        'search': search,
        'result': result
    })

    return HttpResponse(body, content_type='application/json')