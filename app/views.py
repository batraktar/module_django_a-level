from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from app.forms import UserCreateForm, ProductForm, PurchaseForm, ReturnCreate
from app.models import Product, Purchase, Return


class AdminPassedMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class ProductListView(ListView):
    template_name = 'base.html'
    queryset = Product.objects.all()
    paginate_by = 6


class ProductCreateView(LoginRequiredMixin, CreateView):
    login_url = '/'
    form_class = ProductForm
    template_name = 'create_product.html'
    success_url = '/'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'
    extra_context = {'prodquan': PurchaseForm()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PurchaseForm()
        return context


class ProdUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login/'
    model = Product
    form_class = ProductForm
    template_name = 'update_product.html'
    success_url = '/'


class Registration(CreateView):
    template_name = 'registration.html'
    form_class = UserCreateForm
    success_url = '/'


class Login(LoginView):
    template_name = 'log-in.html'
    next_page = '/'


class PurchaseCreate(LoginRequiredMixin, CreateView):
    model = Purchase
    form_class = PurchaseForm
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {'slug': self.kwargs['slug'], 'request': self.request}
        )
        return kwargs

    def form_invalid(self, form):
        return redirect('/')

    def form_valid(self, form):
        obj = form.save(commit=False)
        product = form.product
        obj.product = product
        obj.user = self.request.user
        product.quantity -= obj.prodquan
        self.request.user.wallet -= obj.prodquan * product.price
        with transaction.atomic():
            obj.save()
            product.save()
            self.request.user.save()
        messages.success(self.request, 'Purchase completed successfully!')
        return super().form_valid(form=form)


class PurchaseView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = 'user_purchases.html'
    queryset = Purchase.objects.all()
    login_url = 'login/'
    extra_context = {'form': ReturnCreate}

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class ReturnCreateView(LoginRequiredMixin, CreateView):
    model = Return
    form_class = ReturnCreate
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {'purchase_id': self.kwargs['purchase_id'], 'request': self.request}
        )
        return kwargs

    def form_valid(self, form):
        obj_pur = form.purchase
        obj_ret = Return(purchase=obj_pur)
        obj_ret.save()
        messages.success(self.request, 'Return is done!')
        return redirect('/')

    def form_invalid(self, form):
        return redirect('/purchase/')


class AdminReturnView(AdminPassedMixin, ListView):
    model = Return
    template_name = 'return_list.html'
    queryset = Return.objects.all()
    login_url = 'login/'


class AdminAcceptReturn(AdminPassedMixin, DeleteView):
    model = Purchase
    success_url = '/'

    def form_valid(self, form):
        self.object.product.quantity += self.object.prodquan
        self.object.user.wallet += self.object.prodquan * self.object.product.price
        with transaction.atomic():
            self.object.product.save()
            self.object.user.save()
            return super().form_valid(form=form)


class CancelReturn(AdminPassedMixin, DeleteView):
    model = Purchase
    success_url = '/'


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
