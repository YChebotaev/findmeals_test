from django.views.generic import TemplateView, FormView
from django import forms
from django.http import HttpResponse
import sqlalchemy
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
    search = request.GET.get('search', '')
    include = request.GET.get('include', '[]')
    exclude = request.GET.get('exclude', '[]')

    include = json.loads(include)
    exclude = json.loads(exclude)

    if len(include) > 0:
        include = [x.get('text') for x in include]
    else:
        include = None

    if len(exclude) > 0:
        exclude = [x.get('text') for x in exclude]
    else:
        exclude = None

    search = search.strip()
    if search is '':
        search = None



    if search is not None:
        query = session.query(Recepie)
        query = query.filter(Recepie.display_name.contains(search))
        result = [r.toJSON() for r in query]
    else:
        query = session.query(Ingredient).all()
        ingredients = dict()

        for ingredient in query:
            if include is not None:
                for display_name in include:
                    if display_name == ingredient.display_name:
                        ingredients[ingredient.id] = ingredient

            if exclude is not None:
                for display_name in exclude:
                    if display_name == ingredient.display_name:
                        ingredients[ingredient.id] = None

        result = dict()

        for ingredient in ingredients.values():
            if ingredient is not None:
                for recepie in ingredient.recepies:
                    result[recepie.id] = recepie.toJSON()

        result = list(result.values())

    body = json.dumps({
        'include': include,
        'exclude': exclude,
        'search': search,
        'result': result
    })

    return HttpResponse(body, content_type='application/json')

def ingredients_autocomplete(request):
    search = request.GET.get('query', '')

    query = session.query(Ingredient)
    query = query.filter(Ingredient.display_name.startswith(search))

    result = [{
        'text': r.display_name
    } for r in query]

    body = json.dumps(result)

    return HttpResponse(body, content_type='application/json')