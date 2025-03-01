from django.urls import path
from django.contrib.auth import views as auth_views
from .views import export_colors_excel,custom_logout,dashboard,register,export_colors_csv,search_colors,save_color_data,saved_colors,upload_image, select_area, process_color_selection, detect_gemstone_color, upload_color_data,closest_color

urlpatterns = [
    path('upload/', upload_image, name='upload_image'),
    path('select/<int:image_id>/', select_area, name='select_area'), 
    path('color/closest_color/', closest_color, name='closest_color'), 
    path('saved_colors/', saved_colors, name='saved_colors'),
    path('save_color/', save_color_data, name='save_color_data'),
    path('search_colors/', search_colors, name='search_colors'),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='home'),  # ✅ Homepage is the login page
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),  # ✅ Dashboard page after login
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('logout/', custom_logout, name='logout'),
    path('export_colors_csv/', export_colors_csv, name='export_colors_csv'),
    path('export_colors_excel/', export_colors_excel, name='export_colors_excel'),
    path('process/<int:image_id>/', process_color_selection, name='process_color_selection'),
    path('detect/<int:image_id>/', detect_gemstone_color, name='detect_gemstone_color'),
    path('upload_data/<int:image_id>/', upload_color_data, name='upload_color_data'),
]

