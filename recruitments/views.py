from django.views     import View
from django.http      import JsonResponse

from .models          import *

class CategoryView(View):
    def get(self, request):
        occupation_categories = OccupationCategory.objects.all()

        results = [{
            "id"               : category.id,
            "name"             : category.name,
            "subcategory_list" : [{
                "id"           : subcategory.id,
                "name"         : subcategory.name,                                 
            } for subcategory in category.occupation_subcategories.all()]
        } for category in occupation_categories]

        return JsonResponse({"results" : results}, status = 200)