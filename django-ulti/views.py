from django.shortcuts import render

def custom_error_404(request, exception):
    return render(request, 'weberror/404.html', {})

def custom_error_500(request):
    return render(request, 'weberror/500.html', {})

def custom_error_403(request, exception):
    return render(request, 'weberror/403.html', {})
