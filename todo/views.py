from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import TodoForm
from .models import Todo, Control
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
class HomePageView(TemplateView):
    template_name = "todo/home.html"

@login_required
def get_showing_todos(request, todos, controls):
    if controls.title_order == True:
        title_order_val = 'title'
    else:
        title_order_val = '-title'
    if controls.description_order == True:
        description_order_val = 'description'
    else:
        description_order_val = '-description'
    if controls.complete_order == True:
        is_completed_order_val = 'is_completed'
    else:
        is_completed_order_val = '-is_completed'


    if controls.col_pri == Control.order_by.TITLE:
        print("TITLE order")
        pri_col = title_order_val
        sec_col = description_order_val
        tri_col = is_completed_order_val
    if controls.col_pri == Control.order_by.DESCRIPTION:
        print("DESCRIPTION order")
        pri_col = description_order_val
        sec_col = title_order_val
        tri_col = is_completed_order_val
    if controls.col_pri == Control.order_by.COMPLETE:
        print("COMPLETE order")
        pri_col = is_completed_order_val
        sec_col = title_order_val
        tri_col = description_order_val

    if controls.complete_filter == Control.complete_filters.YES:
        return todos.filter(is_completed=True).order_by(pri_col, sec_col, tri_col)
    if controls.complete_filter == Control.complete_filters.NO:
        return todos.filter(is_completed=False).order_by(pri_col, sec_col, tri_col)
    if controls.complete_filter == Control.complete_filters.ALL:
        return todos.order_by(pri_col, sec_col, tri_col)

@login_required
def index(request):
    todos = Todo.objects.filter(owner=request.user)
    controls = Control.objects.filter(user=request.user)
    if controls.exists():
        controls = controls[0]
    else:
        controls = Control.objects.create(user=request.user)
        return HttpResponseRedirect(reverse('todo:home'))

    completed_count = todos.filter(is_completed=True).count()
    incomplete_count = todos.filter(is_completed=False).count()
    all_count = todos.count()

    context = {'controls':controls, 'todos': get_showing_todos(request, todos, controls), 'all_count': all_count,
               'completed_count': completed_count, 'incomplete_count': incomplete_count}
    return render(request, 'todo/index.html', context)

@login_required
def order_by(request, col_pri_str, asc_dsc=None):
    controls = Control.objects.filter(user=request.user).first()

    if (asc_dsc is not None) and (asc_dsc == 'True'):
        asc_dsc = True
    elif (asc_dsc is not None) and (asc_dsc == 'False'):
        asc_dsc = False

    if col_pri_str == Control.order_by.TITLE:
        controls.col_pri = Control.order_by.TITLE
        if (asc_dsc is None):
            controls.title_order = not controls.title_order
        else:
            controls.title_order = asc_dsc
        # messages.add_message(request, messages.SUCCESS, "Order By {} {}".format(Control.order_by.TITLE, asc_dsc))
    elif col_pri_str == Control.order_by.DESCRIPTION:
        controls.col_pri = Control.order_by.DESCRIPTION
        if (asc_dsc is None):
            controls.description_order = not controls.description_order
        else:
            controls.description_order = asc_dsc
        # messages.add_message(request, messages.SUCCESS, "Order By {} {}".format(Control.order_by.DESCRIPTION, asc_dsc))
    elif col_pri_str == Control.order_by.COMPLETE:
        controls.col_pri = Control.order_by.COMPLETE
        if (asc_dsc is None):
            controls.complete_order = not controls.complete_order
        else:
            controls.complete_order = asc_dsc
        # messages.add_message(request, messages.SUCCESS, "Order By {} {}".format(Control.order_by.COMPLETE, asc_dsc))

    if controls.user == request.user:
        controls.save()
    return HttpResponseRedirect(reverse('todo:home'))

@login_required
def complete_filter_view(request, filter):
    controls = Control.objects.filter(user=request.user).first()
    if filter == Control.complete_filters.ALL:
        controls.complete_filter = Control.complete_filters.ALL
    elif filter == Control.complete_filters.NO:
        controls.complete_filter = Control.complete_filters.NO
    elif filter == Control.complete_filters.YES:
        controls.complete_filter = Control.complete_filters.YES
    # messages.add_message(request, messages.SUCCESS, "COMPLETE - {}".format(controls.complete_filter))

    if controls.user == request.user:
        # print(controls.title_order)
        # print(controls.description_order)
        # print(controls.complete_order)
        # print(controls.col_pri)
        # print(controls.complete_filter)

        controls.save()
    return HttpResponseRedirect(reverse('todo:home'))

@login_required
def create_todo(request):
    form = TodoForm()
    context = {'form': form}

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_completed = request.POST.get('is_completed', False)

        todo = Todo()

        todo.title = title
        todo.description = description
        todo.is_completed = True if is_completed == "on" else False
        todo.owner = request.user
        todo.save()

        messages.add_message(request, messages.SUCCESS, "Todo created successfully")

        return HttpResponseRedirect(reverse("todo:todo", kwargs={'id': todo.pk}))

    return render(request, 'todo/create-todo.html', context)

@login_required
def todo_detail(request, id):
    todo = get_object_or_404(Todo, pk=id)
    context = {'todo': todo}
    return render(request, 'todo/todo-detail.html', context)

@login_required
def todo_delete(request, id):
    todo = get_object_or_404(Todo, pk=id)
    context = {'todo': todo}

    if request.method == 'POST':
        if todo.owner == request.user:
            todo.delete()
            messages.add_message(request, messages.SUCCESS, "Todo deleted successfully"
                                 )
            return HttpResponseRedirect(reverse('todo:home'))
        return render(request, 'todo/todo-delete.html', context)

    return render(request, 'todo/todo-delete.html', context)

@login_required
def todo_edit(request, id):
    todo = get_object_or_404(Todo, pk=id)
    form = TodoForm(instance=todo)
    context = {'todo': todo, 'form': form}

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_completed = request.POST.get('is_completed', False)

        todo.title = title
        todo.description = description
        todo.is_completed = True if is_completed == "on" else False

        if todo.owner == request.user:
            todo.save()

        messages.add_message(request, messages.SUCCESS, "Todo update success"

                             )

        return HttpResponseRedirect(reverse("todo:todo", kwargs={'id': todo.pk}))

    return render(request, 'todo/todo-edit.html', context)
