from django.shortcuts import render, redirect


# Create your views here.
def index(request):
	if request.user.is_authenticated:
		try:
			if request.user.doctor.role == "Doctor":
				return redirect('/doctor/search_patient/')
			if request.user.manager.role == "Manager":
				return redirect('/manager/')
		except Exception as e:
			print(e)
	return render(request, 'pages/index.html')