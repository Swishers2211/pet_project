from django.shortcuts import render, Http404, HttpResponseRedirect, reverse, redirect
from django.contrib.auth.decorators import login_required

from home.models import Category, Game, SubCategory, SellProduct, Product, Category_Game, PlatForms, Basket
from users.models import User

from home.forms import ProductForm

def home(request):
	context = {
		'games': Game.objects.all().order_by('-published')[:12],
		'categories': Category.objects.all(),
	}
	return render(request, 'home/index.html', context)

def detail_game(request, game_id):
	try:
		game = Game.objects.get(id=game_id)
	except:
		raise Http404('Игра не найдена!')

	context = {
		'game': game,
		'categories': Category.objects.filter(game=game_id),
		# 'products': Product.objects.filter(category=game_id),
		# 'platforms': PlatForms.objects.all(category_id=game_id),
	}
	return render(request, 'home/detail_game.html', context)

def detail_category(request, category_id):
	try:
		categories = Category.objects.get(id=category_id)
	except:
		raise Http404('Категория не найдена!')

	context = {
		'categories': categories,
		'categoriess': Category.objects.filter(game=categories.game.id).order_by('name'),
		'subcategories': SubCategory.objects.filter(category_id=categories),
		'sell_products': SellProduct.objects.filter(category_id=categories),
		'products': Product.objects.filter(category_id=categories).order_by('-published'),
		'platforms': PlatForms.objects.filter(category_id=categories),
	}
	return render(request, 'home/detail_category_products.html', context)

def create_product(request, game_id):
	try:
		game = Game.objects.get(id=game_id)
	except:
		raise Http404('Игра не найдена!')
	if request.method == 'POST':
		form = ProductForm(data=request.POST, category=game.id)
		form.instance.user = request.user
		if form.is_valid():
			form.save()
			return redirect('home')
	else:
		form = ProductForm(category=game.id)
	context = {
		'form': form,
		'game': game,
	}
	return render(request, 'home/create_product.html', context)

def search_by_games(request):
	context = {
		'games': Game.objects.all().order_by('-published')[:12],
		'category_games': Category_Game.objects.all(),
	}
	return render(request, 'home/search-games.html', context)

def detail_category_game(request, category_id):
	try:
		categories = Category_Game.objects.get(id=category_id)
	except:
		raise Http404('Категория не найдена!')


	context = {
		'categories': categories,
		'category_games': Category_Game.objects.all().order_by()[:12],
		'games': Game.objects.filter(category_game_id=categories.id),
	}
	return render(request, 'home/detail_category.html', context)

def detail_product(request, product_id):
	try:
		product = Product.objects.get(id=product_id)
	except:
		raise Http404('Товар не найдена!')

	context = {
		'product': product,
		'products': Product.objects.filter(id=product_id),
		# 'platforms': PlatForms.objects.all(category_id=game_id),
	}
	return render(request, 'home/detail_product.html', context)

def basket_list(request):
	context = {
		'baskets': Basket.objects.filter(user=request.user).order_by('-published'),
	}
	return render(request, 'home/baskets.html', context)

def basket_product_detail(request, product_id):
	try:
		basket = Basket.objects.get(id=product_id)
	except:
		raise Http404('Товар не найден!')

	context = {
		'basket': basket,
	}
	return render(request, 'home/basket_product_detail.html', context)

@login_required
def basket_add(request, product_id):
	Basket.create_or_update(product_id, request.user)
	return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def basket_remove(request, basket_id):
	basket = Basket.objects.get(id=basket_id)
	basket.delete()
	return HttpResponseRedirect(request.META['HTTP_REFERER'])