from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
from django.contrib.auth.decorators import login_required
from .forms import GemstoneImageForm
from .models import GemstoneImage, ColorAnalysis
import cv2,io,base64,json,csv
import numpy as np
from django.core.files.base import ContentFile
from PIL import Image
from .color_utils import get_color_name

from django.http import JsonResponse
from .models import GemstoneImage, ColorAnalysis
from django.views.decorators.csrf import csrf_exempt 
from .color_utils import get_color_name
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect,HttpResponse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout

import json,csv,os,datetime

from openpyxl import Workbook
from openpyxl.drawing.image import Image as ExcelImage
from django.conf import settings




@login_required
def upload_image(request):
    gemstone = None  # Initialize gemstone as None

    if request.method == 'POST':
        form = GemstoneImageForm(request.POST, request.FILES)
        if form.is_valid():
            gemstone = form.save(commit=False)
            gemstone.user = request.user
            gemstone.save()
            return redirect('select_area', image_id=gemstone.id)  # Redirect to selection page

    else:
        form = GemstoneImageForm()

    return render(request, 'upload.html', {'form': form, 'gemstone': gemstone})

@login_required
def select_area(request, image_id):
    gemstone = get_object_or_404(GemstoneImage, id=image_id)
    return render(request, 'select_area.html', {'gemstone': gemstone})


@login_required
def process_color_selection(request, image_id):
    if request.method == 'POST':
        gemstone = GemstoneImage.objects.get(id=image_id)
        x, y, w, h = map(int, request.POST.getlist('coords'))
        
        # Read the image
        img = cv2.imread(gemstone.image.path)
        cropped_img = img[y:y+h, x:x+w]
        
        # Convert to RGB and get the mean color
        avg_color = np.mean(cropped_img, axis=(0,1))
        avg_color = tuple(map(int, avg_color[::-1]))  # Convert to (R, G, B)
        
        # Get the top 3 closest color names
        color_predictions = get_color_name(avg_color)

        # Save to database
        analysis = ColorAnalysis.objects.create(
            gemstone_image=gemstone,
            selected_color=str(avg_color),
            color_percentage=color_predictions
        )
        return redirect('color_result', analysis.id)
    return redirect('upload_image')

@login_required
def color_result(request, analysis_id):
    analysis = ColorAnalysis.objects.get(id=analysis_id)
    return render(request, 'color_result.html', {'analysis': analysis})



@csrf_exempt
def closest_color(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rgb = tuple(data.get("color", []))  # Extract RGB values

            print(f"Received RGB: {rgb}")  # ✅ Debugging: Log received values

            if len(rgb) != 3:
                return JsonResponse({'error': 'Invalid RGB format, expected [R, G, B]'}, status=400)

            closest_matches = get_color_name(rgb)

            print(f"Closest Matches: {closest_matches}")  # ✅ Debugging: Log matched colors

            return JsonResponse({'colors': closest_matches})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)



@csrf_exempt
def save_color_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            print("✅ Received Data:", data)  # Debugging

            image_id = data.get("image_id")
            rgb = tuple(data.get("rgb", []))
            css_color_code = data.get("css_color_code", "")
            brightness = data.get("brightness", 0)
            color_ratios = data.get("color_ratios", "")
            density = data.get("density", 0)

            if not image_id or len(rgb) != 3:
                print("⚠️ Invalid image ID or RGB values!")  # Debugging
                return JsonResponse({'error': 'Invalid data provided'}, status=400)

            try:
                gemstone_image = GemstoneImage.objects.get(id=image_id)
            except GemstoneImage.DoesNotExist:
                print("⚠️ Image ID not found in the database!")  # Debugging
                return JsonResponse({'error': 'Image not found'}, status=400)

            closest_matches = get_color_name(rgb)

            # Save data
            color_analysis = ColorAnalysis.objects.create(
                gemstone_image=gemstone_image,
                rgb=str(rgb),
                css_color_code=css_color_code,
                brightness=brightness,
                color_ratios=color_ratios,
                density=density,
                closest_colors=closest_matches
            )

            print(f"✅ Data saved successfully! Color ID: {color_analysis.id}")  # Debugging
            return JsonResponse({'message': 'Color data saved successfully!', 'color_id': color_analysis.id})

        except Exception as e:
            print(f"❌ Error saving data: {e}")  # Debugging
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)



@csrf_exempt
def save_color_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            print("✅ Received Data:", data)  # Debugging

            image_id = data.get("image_id")
            rgb = tuple(data.get("rgb", []))
            css_color_code = data.get("css_color_code", "")
            brightness = data.get("brightness", 0)
            color_ratios = data.get("color_ratios", "")
            density = data.get("density", 0)

            if not image_id or len(rgb) != 3:
                print("⚠️ Invalid image ID or RGB values!")  # Debugging
                return JsonResponse({'error': 'Invalid data provided'}, status=400)

            try:
                gemstone_image = GemstoneImage.objects.get(id=image_id)
            except GemstoneImage.DoesNotExist:
                print("⚠️ Image ID not found in the database!")  # Debugging
                return JsonResponse({'error': 'Image not found'}, status=400)

            closest_matches = get_color_name(rgb)

            # Save data
            color_analysis = ColorAnalysis.objects.create(
                gemstone_image=gemstone_image,
                rgb=str(rgb),
                css_color_code=css_color_code,
                brightness=brightness,
                color_ratios=color_ratios,
                density=density,
                closest_colors=closest_matches
            )

            print(f"✅ Data saved successfully! Color ID: {color_analysis.id}")  # Debugging
            return JsonResponse({'message': 'Color data saved successfully!', 'color_id': color_analysis.id})

        except Exception as e:
            print(f"❌ Error saving data: {e}")  # Debugging
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)



def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # ✅ Automatically log in after registering
            return redirect("/")  # ✅ Redirect to homepage
    else:
        form = UserCreationForm()
    
    return render(request, "register.html", {"form": form})

def search_colors(request):
    query = request.GET.get("q", "")
    filter_by = request.GET.get("filter_by", "all")
    
    colors = ColorAnalysis.objects.all()

    # Search logic
    if query:
        if filter_by == "rgb":
            colors = colors.filter(Q(rgb__icontains=query))
        elif filter_by == "css":
            colors = colors.filter(Q(css_color_code__icontains=query))
        elif filter_by == "brightness":
            colors = colors.filter(Q(brightness__gte=query))
        elif filter_by == "color_ratios":
            colors = colors.filter(Q(color_ratios__icontains=query))
        elif filter_by == "density":
            colors = colors.filter(Q(density__gte=query))
        elif filter_by == "top_color":
            colors = colors.filter(Q(closest_colors__icontains=query))
        else:
            colors = colors.filter(
                Q(rgb__icontains=query) |
                Q(css_color_code__icontains=query) |
                Q(color_ratios__icontains=query) |
                Q(density__gte=query) |
                Q(brightness__gte=query) |
                Q(closest_colors__icontains=query)
            )

    return render(request, "search_colors.html", {"colors": colors, "query": query, "filter_by": filter_by})







def export_colors_excel(request):
    """ Export gemstone images and solid color images to an Excel file (.xlsx) """
    wb = Workbook()
    ws = wb.active
    ws.title = "Gemstone Colors"

    # ✅ Add headers
    headers = ["ID", "Gemstone Image", "Solid Color", "CSS Color Code", "RGB", "Brightness", "Color Ratios", "Density", "Created At"]
    ws.append(headers)

    colors = ColorAnalysis.objects.all()
    row_num = 2  # Excel row number (starting after the header)

    solid_colors_folder = os.path.join(settings.MEDIA_ROOT, "solid_colors")
    os.makedirs(solid_colors_folder, exist_ok=True)  # ✅ Ensure folder exists

    for color in colors:
        # ✅ Convert timezone-aware datetime to timezone-naive format
        created_at_naive = color.created_at.replace(tzinfo=None) if color.created_at else ""

        # ✅ Insert data into cells
        ws.append([
            color.id, "", "", color.css_color_code, color.rgb, color.brightness, color.color_ratios, color.density, created_at_naive
        ])

        # ✅ Load and insert gemstone image
        if color.gemstone_image.image:
            img_path = os.path.join(settings.MEDIA_ROOT, color.gemstone_image.image.name)
            if os.path.exists(img_path):
                img = ExcelImage(img_path)
                img.width = 100
                img.height = 100
                ws.add_image(img, f"B{row_num}")  # ✅ Insert gemstone image in column B

        # ✅ Generate solid color image
        solid_color_path = os.path.join(solid_colors_folder, f"solid_{color.id}.png")

        solid_color_img = Image.new("RGB", (100, 100), color.css_color_code)
        solid_color_img.save(solid_color_path)

        # ✅ Insert solid color image
        solid_img = ExcelImage(solid_color_path)
        solid_img.width = 100
        solid_img.height = 100
        ws.add_image(solid_img, f"C{row_num}")  # ✅ Insert solid color image in column C

        row_num += 1  # Move to the next row

    # ✅ Generate response as an Excel file
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="colors.xlsx"'
    wb.save(response)
    return response





def export_colors_csv(request):
    """ Export color data including image and solid color to CSV """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="colors.csv"'

    writer = csv.writer(response)
    # ✅ Add new columns for gemstone image and solid color
    writer.writerow(['ID', 'Gemstone Image', 'Solid Color (CSS)', 'RGB', 'Brightness', 'Color Ratios', 'Density', 'Created At'])

    colors = ColorAnalysis.objects.all()
    for color in colors:
        writer.writerow([
            color.id,
            color.gemstone_image.image.url,  # ✅ Path to gemstone image
            color.css_color_code,  # ✅ Solid color (CSS)
            color.rgb,
            color.brightness,
            color.color_ratios,
            color.density,
            color.created_at,
        ])

    return response

@login_required  # ✅ Ensure only logged-in users can access the dashboard
def dashboard(request):
    return render(request, "dashboard.html", {"user": request.user})

def process_color_selection(request, image_id):
    if request.method == 'POST':
        gemstone = GemstoneImage.objects.get(id=image_id)
        x, y, w, h = map(int, request.POST.get('coords').split(','))

        img = cv2.imread(gemstone.image.path)
        cropped_img = img[y:y+h, x:x+w]

        avg_color = np.mean(cropped_img, axis=(0,1))
        avg_color = tuple(map(int, avg_color[::-1]))

        brightness = round(sum(avg_color) / 3, 2)
        color_ratios = [round(c / sum(avg_color), 2) for c in avg_color]

        return JsonResponse({
            'rgb': avg_color,
            'brightness': brightness,
            'ratios': color_ratios
        })


def custom_logout(request):
    if request.method == "POST" or request.method == "GET":  # ✅ Allow both POST and GET requests
        logout(request)
        return redirect("login")  # ✅ Redirect to login page after logout
    else:
        return HttpResponseRedirect("/")

def detect_gemstone_color(request, image_id):
    gemstone = GemstoneImage.objects.get(id=image_id)
    analysis = ColorAnalysis.objects.filter(gemstone_image=gemstone).first()

    if analysis:
        return JsonResponse({'colors': analysis.color_percentage})
    return JsonResponse({'error': 'No color analysis found'})

def upload_color_data(request, image_id):
    if request.method == 'POST':
        gemstone = GemstoneImage.objects.get(id=image_id)
        rgb = request.POST['rgb']
        brightness = request.POST['brightness']
        ratios = request.POST['ratios']

        ColorAnalysis.objects.create(
            gemstone_image=gemstone,
            selected_color=rgb,
            color_percentage=get_color_name(eval(rgb)),  
            brightness=brightness
        )
        
        return redirect('color_result', image_id)


def saved_colors(request):
    colors = ColorAnalysis.objects.all().order_by('-created_at')  # Show latest first
    return render(request, 'saved_colors.html', {'colors': colors})