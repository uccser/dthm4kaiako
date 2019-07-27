import random
from poet.models import Resource


def select_resources_for_poet_form(request):
        random.sample(list(Resource.objects.all()), 3)
        resources = random.sample(list(Resource.objects.all()), 3)
        return resources
