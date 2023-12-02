from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Quote, Author

def quotes_list(request):
    quote_list = Quote.objects.all().order_by('id')  # Show 10 quotes per page.

    paginator = Paginator(quote_list, 10)

    page = request.GET.get('page')
    try:
        quotes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        quotes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        quotes = paginator.page(paginator.num_pages)

    return render(request, 'quotes/quotes_list.html', {'quotes': quotes})

def quote_detail(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    return render(request, 'quotes/quote_detail.html', {'quote': quote})

def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, 'quotes/author_detail.html', {'author': author})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})