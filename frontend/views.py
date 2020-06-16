from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from listings.models import Listing
from members.models import Member

@login_required
def list(request):
	if request.user.is_authenticated:
		my_qs = Member.objects.filter(username=request.user)
		qs = Listing.objects.filter(contributor=my_qs[0])
		context = {"title": "List.html", 'my_qs': my_qs}
		return render(request, "frontend/list.html", context)