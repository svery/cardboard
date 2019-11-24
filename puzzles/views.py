from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Puzzle
from .forms import StatusForm
from answers.models import Answer
from answers.forms import AnswerForm
from django.http import HttpResponseRedirect

@login_required(login_url='/accounts/login/')
def puzzle_page(request, pk):
    puzzle = Puzzle.objects.get(pk=pk)
    context = {
        'puzzle': puzzle,
        'form': form
    }
    return render(request, 'puzzle_page.html', context)


@login_required(login_url='/accounts/login/')
def update_status(request, pk):
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=Puzzle.objects.get(pk=pk))
        if form.is_valid():
            form.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='/accounts/login/')
def guess(request, pk):
    print("guessing!")
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        puzzle = Puzzle.objects.get(pk=pk)

        if form.is_valid() and puzzle.status != Puzzle.SOLVED:
            answer = Answer(text=form.cleaned_data["text"], puzzle=puzzle)
            puzzle.status = Puzzle.PENDING
            answer.save()
            puzzle.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
