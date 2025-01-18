import json
import re
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Post
from django.core.paginator import Paginator
from datetime import datetime

# Create your views here.
from django.http import HttpResponse, JsonResponse
print("Inside")



def index(request):
    print("inside index",request)
    
    res = HttpResponse("Hello, world. You're at the polls index.") ;
    print(res)
    return  res#seen in postman
    

print("outside")

@csrf_exempt
def create_posts(request):
    print("Inside Create_Posts", request)

    if request.method == "POST":
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)

            # Check if required fields are present in the body
            required_fields = ["reference_number", "name", "email", "phone_number", "dob", "idproof"]
            missing_fields = [field for field in required_fields if field not in data]

            if missing_fields:
                return JsonResponse(
                    {"status": "error", "message": f"Missing fields: {', '.join(missing_fields)}"},
                    status=400
                )

            # Save the received data into the database
            post = Post.objects.create(
                reference_number=data["reference_number"],
                name=data["name"],
                email=data["email"],
                phone_number=data["phone_number"],
                dob=data["dob"],
                idproof=data["idproof"]
            )

            # Fetch the saved data from the database (if you want to return the saved record)
            saved_post = Post.objects.get(id=post.id)

            response_data = {
                "status": "success",
                "message": "Details submitted successfully",
                "reference_number": saved_post.reference_number,
                "name": saved_post.name,
                "email": saved_post.email,
                "phone_number": saved_post.phone_number,
                "dob": saved_post.dob,
                "idproof": saved_post.idproof
            }

            print("Outside Create_Posts")

            return JsonResponse(response_data, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON in request body"}, status=400)

    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)  



def read_lists_posts(request):
    print("Inside read = lists = posts")  

    
    # Parse query parameters
    page = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page", 10))
    order_by = request.GET.get("order_by", "id")
    order_method = request.GET.get("order_method", "asc")
    search_condition = request.GET.get("search_condition", "and")
    equal = request.GET.get("equal")
    not_equal = request.GET.get("not")
    like = request.GET.get("like")
    date_range_by = request.GET.get("date_range_by", "dob")
    date_start = request.GET.get("date_start")
    date_end = request.GET.get("date_end")
    
    print(f"Parameters received: page={page}, per_page={per_page}, order_by={order_by}, "
          f"order_method={order_method}, search_condition={search_condition}, equal={equal}, "
          f"not={not_equal}, like={like}, date_range_by={date_range_by}, date_start={date_start}, date_end={date_end}")
    
    # Validate mandatory parameters
    if page < 1 or per_page < 1 or per_page > 25:
        print("Invalid page or per_page value")
        return JsonResponse({"status": "error", "message": "Invalid page or per_page value"}, status=400)

    if not re.match(r'^[a-zA-Z_]+$', order_by):
        print("Invalid order_by value")
        return JsonResponse({"status": "error", "message": "Invalid order_by value"}, status=400)

    if order_method not in ["asc", "desc"]:
        print("Invalid order_method value")
        return JsonResponse({"status": "error", "message": "Invalid order_method value"}, status=400)

    # Queryset initialization
    queryset = Post.objects.all()
    print(f"Initial queryset count: {queryset.count()}")

    # Apply filters
    if equal:
        queryset = queryset.filter(reference_number=equal)
        print(f"Filtered queryset by 'equal': {queryset.count()} records")
    if not_equal:
        queryset = queryset.exclude(reference_number=not_equal)
        print(f"Filtered queryset by 'not_equal': {queryset.count()} records")
    if like:
        queryset = queryset.filter(reference_number__icontains=like)
        print(f"Filtered queryset by 'like': {queryset.count()} records")

    # Date range filter
    if date_start and date_end:
        try:
            start_date = datetime.strptime(date_start, "%Y-%m-%d")
            end_date = datetime.strptime(date_end, "%Y-%m-%d")
            queryset = queryset.filter(**{f"{date_range_by}__range": (start_date, end_date)})
            print(f"Filtered queryset by date range: {queryset.count()} records")
        except ValueError as e:
            print(f"Date parsing error: {e}")
            return JsonResponse({"status": "error", "message": "Invalid date format"}, status=400)

    # Apply ordering
    if order_method == "desc":
        order_by = f"-{order_by}"
    queryset = queryset.order_by(order_by)
    print(f"Ordered queryset: {queryset.count()} records")

    # Apply pagination
    paginator = Paginator(queryset, per_page)
    try:
        page_obj = paginator.page(page)
        print(f"Page {page} retrieved with {len(page_obj.object_list)} records")
    except Exception as e:
        print(f"Pagination error: {e}")
        return JsonResponse({"status": "error", "message": "Page number out of range"}, status=400)

    # Prepare response
    data = [
        {
            "id": post.id,
            "reference_number": post.reference_number,
            "name": post.name,
            "email": post.email,
            "phone_number": post.phone_number,
            "dob": post.dob,
            "idproof": post.idproof,
        }
        for post in page_obj.object_list
    ]
    response_data = {
        "status": "success",
        "data": data,
        "total_pages": paginator.num_pages,
        "current_page": page,
    }

    print("Outside read list")

    print(f"Response data prepared: {response_data}")
    return JsonResponse(response_data, status=200)
      





@csrf_exempt
def put_posts_id(request, id):
    print("Inside Put_Post_Id")
    
    if request.method == "PUT":
        try:
            # Log the raw body
            print(f"Raw request body: {request.body}")
            
            # Decode and parse JSON
            data = json.loads(request.body.decode('utf-8'))
            print(f"Parsed JSON: {data}")
            
            # Validate required fields
            required_fields = ["id", "reference_number", "name", "email", "phone_number", "dob", "idproof"]
            for field in required_fields:
                if field not in data:
                    print(f"Missing required field: {field}")
                    return JsonResponse({
                        "status": "error",
                        "message": f"Missing required field: {field}"
                    }, status=400)
            
            # Ensure the ID matches
            if data["id"] != id:
                print("ID mismatch between URL and request body")
                return JsonResponse({
                    "status": "error",
                    "message": "ID mismatch between URL and request body"
                }, status=400)
            
            # Simulated update logic
            print(f"Updating post with ID: {id}")
            updated_data = {
                "id": id,
                "reference_number": data["reference_number"],
                "name": data["name"],
                "email": data["email"],
                "phone_number": data["phone_number"],
                "dob": data["dob"],
                "idproof": data["idproof"]
            }
            print(f"Updated data: {updated_data}")
            
            return JsonResponse({
                "status": "success",
                "message": "Post updated successfully",
                "data": updated_data
            }, status=200)
        
        except json.JSONDecodeError as e:
            # Log invalid JSON error
            print(f"JSONDecodeError: {e}")
            return JsonResponse({
                "status": "error",
                "message": "Invalid JSON payload. Ensure the body contains properly formatted JSON."
            }, status=400)
        
        except Exception as e:
            # Log unexpected errors
            print(f"Unhandled exception: {e}")
            return JsonResponse({
                "status": "error",
                "message": "An internal error occurred. Please try again later."
            }, status=500)
    
    print("Invalid HTTP method")
    return JsonResponse({
        "status": "error",
        "message": "Invalid HTTP method. Use PUT for this endpoint."
    }, status=405)




@csrf_exempt
def delete_posts_id(request, id):
    print("Inside Delete_Post_Id")

    if request.method == "DELETE":
        print("Using DELETE method")

        # Perform the actual deletion logic here
        response_data = {"status": "success", "message": "Post deleted successfully."}
        return JsonResponse(response_data, status=200)

    # If method is not DELETE, return 405 Method Not Allowed
    response_data = {"status": "error", "message": "Invalid HTTP method. Use DELETE for this endpoint."}
    return JsonResponse(response_data, status=405)




