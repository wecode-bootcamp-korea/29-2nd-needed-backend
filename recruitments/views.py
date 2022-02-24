from django.views        import View
from django.http         import JsonResponse
from django.db.models    import Q, Prefetch

from recruitments.models import OccupationCategory,Recruitment, OccupationSubcategory
from companies.models    import Company, Tag


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

class SubCategoryView(View):
    def get(self, request):
        search = request.GET.get('search',None)            
        q = Q()

        if search:
            q = Q(name__icontains = search)

        subcategories = OccupationSubcategory.objects.filter(q)

        results = [{
            "id" : subcategory.id,
            "name" : subcategory.name
        }for subcategory in subcategories]

        return JsonResponse({"results" : results}, status = 200)


class RecruitmentsList(View):
    def get(self,request):
        try:
            filters = {
                'category'    : 'occupation_subcategory__occupation_category__in',
                'subcategory' : 'occupation_subcategory__in',
                'tag'         : 'company__tag_companies__tag__in',
                'country'     : 'company__detail_area__province__country__name__in',
                'location'    : 'company__detail_area__province__name__in',
                'detail'      : 'company__detail_area__name__in'
            }
            
            filter_set = {
                filters.get(key) : value for (key,value) in dict(request.GET).items() if filters.get(key)
            }
            search           = request.GET.get('search',None)
            q = Q()

            if search:
                q = Q(name__icontains = search)
            
            recruitments = Recruitment.objects \
                .order_by(request.GET.get("sort",'id')) \
                .select_related('company__detail_area__province__country') \
                .prefetch_related('company__tag_companies__tag','company__company_images') \
                .filter(q, **filter_set)
                
            result = [{
                "id"           : recruitment.id,
                "name"         : recruitment.name,
                "compensation" : recruitment.compensation,
                "company_name" : recruitment.company.name,
                "country"      : recruitment.company.detail_area.province.country.name,
                "province"     : recruitment.company.detail_area.province.name,
                "logo_image"   : [{'image' : image.image_url} for image in recruitment.company.company_images.all()][0]
            }for recruitment in recruitments]
        
            return JsonResponse({'message':'SUCCESS' ,'Recruitment' : result}, status=200)
        
        except ValueError:
            return JsonResponse({'message':'VALUE_ERROR'}, status=400)

class RecruitmentsDetailView(View):
    def get(self, request, recruitment_id):
        try:
            recruitment = Recruitment.objects \
                .select_related('company__detail_area__province__country') \
                .prefetch_related('company__tag_companies__tag','company__company_images') \
                .get(id = recruitment_id)

            result = {
                "id"                        : recruitment.id,
                "name"                      : recruitment.name,
                "deadline"                  : recruitment.deadline,
                "address"                   : recruitment.address,
                "description"               : recruitment.description,
                "compensation"              : recruitment.compensation,
                "company_id"                : recruitment.company.id,
                "company_name"              : recruitment.company.name,
                "country"                   : recruitment.company.detail_area.province.country.name,
                "province"                  : recruitment.company.detail_area.province.name,
                "occupation_subcategory_id" : recruitment.occupation_subcategory.id,
                "image"                     : [{'image' : image.image_url} for image in recruitment.company.company_images.all()],
                "tags"                      : [{'tag' : tag.name } for tag in recruitment.company.tags.all()]
            }
            
            return JsonResponse({'message':'SUCCESS' ,'result' : result}, status=200)
        
        except ValueError:
            return JsonResponse({'message':'VALUE_ERROR'}, status=400)
        
        except Recruitment.DoesNotExist:
            return JsonResponse({'message':'DOES_NOT_EXIST_RECRUITMENT'}, status=404)
