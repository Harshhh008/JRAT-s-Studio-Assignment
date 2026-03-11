from django.shortcuts import redirect
def home(request):
  return redirect('list_product')