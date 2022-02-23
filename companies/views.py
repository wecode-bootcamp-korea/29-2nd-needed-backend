import json

from django.views         import View
from django.http          import JsonResponse
from django.db.models     import Q

from companies.models      import Company
        
class CompanyView(View):
    def get(self, request, company_id):
        try:
            search = request.GET.get('search',None)
            q = Q()

            if search:
                q = Q(name__icontains = search)

            company = Company.objects \
                                .filter(q) \
                                .prefetch_related('company_images','tags','recruitments') \
                                .get(id = company_id)
                                
            result  = {
                'id'           : company.id,
                'name'         : company.name,
                'description'  : company.description,
                'images'       : [{'image' : image.image_url} for image in company.company_images.all()],
                'tags'         : [{'name'  : tag.name}  for tag in company.tags.all()],
                'recruitments' : [{
                        'id'           : recruitment.id,
                        'name'         : recruitment.name,    
                        'compensation' : recruitment.compensation,
                        'deadline'     : recruitment.deadline,
                    }for recruitment in company.recruitments.all()]
                }
            return JsonResponse({"message" : 'SUCCESS', 'result' : result}, status=200)
        
        except Company.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_EXIST_COMPANY'}, status = 404)
