from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User, Flashcard, Deck
from .forms import DeckForm, CardForm


# Create your views here.
def index(request):
    return render(request, "flashcard/index.html")

@login_required
def list_all_decks(request):
    decks = Deck.objects.all().order_by("title")
    user = get_object_or_404(User, username=request.user)
    user_decks = user.decks.filter()
    return render(request, "flashcard/list_all_decks.html", {"decks": user_decks})

@login_required
def list_all_cards(request):
    cards = Flashcard.objects.all()
    return render(request, "flashcard/list_all_cards.html", {"cards": cards})

@login_required
def view_deck(request, pk):
    deck = get_object_or_404(Deck, id=pk)
    return render(request, "flashcard/view_deck.html", {"deck": deck})

@login_required
def create_deck(request):
    if request.method == "POST":
        form = DeckForm(data=request.POST)
        if form.is_valid():
            deck = form.save(commit=False)
            deck.user = request.user
            deck.save()
            return redirect("create_card")
    else:
        form = DeckForm()
    body = {"form": form}
    return render(request, "flashcard/create_deck.html", body)

@login_required
def create_card(request):
    if request.method == "POST":
        form = CardForm(data=request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.save()
            return redirect("create_card")
    else:
        form = CardForm()
    body = {"form": form}
    return render(request, "flashcard/create_card.html", body)

@login_required
def play_deck(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    if deck.user == request.user:
        return render(request, "flashcard/play_deck.html", {"deck": deck})
    




