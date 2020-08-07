from django.shortcuts import render


# results = Group.objects.filter(name='group1')
# members = results.members.all()
def home(request):
	return render(request, 'main/base.html')

def test(request):
	return render(request, 'main/test.html', {'members': members})
