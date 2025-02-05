from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from .forms import FaqForm
from .models import Faq
from projects.models import Project
from django.contrib.auth.models import User


def index(request, slug):
    account = request.user
    project = get_object_or_404(Project, slug=slug)
    if request.POST:
        if not request.user.is_authenticated:
            messages.error(request, "請先登入")
            return redirect("projects:faq_index", slug=project.slug)
        form = FaqForm(request.POST)
        if form.is_valid():
            faq = form.save(commit=False)
            faq.project = project
            faq.created_by = request.user
            faq.save()
            messages.success(request, "新增成功")
            return redirect("projects:faq_index", slug=project.slug)

    faqs = Faq.objects.filter(project=project, deleted_at__isnull=True)

    # 如果是htmx請求，返回projects下的內容模板
    if request.headers.get("HX-Request"):
        return render(
            request,
            "projects/partials/faq_content.html",
            {"faqs": faqs, "account": account},
        )
    if project.account != request.user:
        messages.error(request, "您無權訪問該頁面")
        return redirect("projects:public", slug=project.slug)

    return render(
        request,
        "faqs/index.html",
        {"faqs": faqs, "project": project, "account": account},
    )


@login_required
def new(request, slug):
    project = get_object_or_404(Project, slug=slug, account=request.user)
    form = FaqForm()
    return render(request, "faqs/new.html", {"form": form, "project": project})


@login_required
def show(request, slug):
    faq = get_object_or_404(Faq, slug=slug, created_by=request.user)
    project = faq.project
    if request.POST:
        form = FaqForm(
            request.POST,
            instance=faq,
        )
        form.save()
        messages.success(request, "更新成功")
        return redirect("projects:faq_index", slug=project.slug)

    return render(
        request,
        "faqs/show.html",
        {
            "faq": faq,
            "project": project,
        },
    )


@login_required
def edit(request, slug):
    faq = get_object_or_404(Faq, slug=slug, created_by=request.user)
    project = faq.project
    form = FaqForm(instance=faq)
    return render(
        request,
        "faqs/edit.html",
        {
            "faq": faq,
            "form": form,
            "project": project,
        },
    )


@login_required
def delete(request, slug):
    faq = get_object_or_404(Faq, slug=slug, created_by=request.user)
    project = faq.project
    if request.POST:
        faq.deleted_at = timezone.now()
        faq.save()
        messages.success(request, "刪除成功")
        return redirect("projects:faq_index", slug=project.slug)

    return render(
        request,
        "faqs/delete.html",
        {
            "faq": faq,
            "project": project,
        },
    )


@csrf_exempt
@require_POST
def updated_faq_position(request):
    import json

    data = json.loads(request.body)
    position = data.get("position", [])
    for index, faq_id in enumerate(position):
        Faq.objects.filter(id=faq_id).update(position=index)
    return JsonResponse({"status": "success"})
