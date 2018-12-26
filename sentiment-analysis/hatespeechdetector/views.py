from django.shortcuts import render
from .forms import QueryForm
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from .logic import examine


def index(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = QueryForm(request.POST)
        # check whether it's valid:
        print("in view")
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            print(form.cleaned_data)
            query = form.cleaned_data["query"]
            (values, pic) = examine(query)
            return render(request, 'hatespeechdetector/results.html',{'positive':values[0],'negative':values[1], 'pic':pic})
    else:
        form = QueryForm()
        return render(request, 'hatespeechdetector/query.html', {'form': form})