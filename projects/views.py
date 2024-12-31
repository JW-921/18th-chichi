from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProjectFrom
from .models import Project, CollectProject, FavoritePrject
from django.utils.timezone import localtime
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.http import HttpResponse
from django.contrib import messages

@login_required
def index(request):
    account = request.user
    if request.POST:
        form = ProjectFrom(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.account = account
            project.save()
            return redirect("projects:index")
        else:
            return HttpResponse("輸入錯誤")

    projects = Project.objects.filter(account=account)
    for project in projects:
        project.update_status()  # 更新專案的上下架狀態
    return render(request, "projects/index.html", {"projects":projects,"account":account})
        
@login_required
def new(request):
    account = request.user
    return render(request, "projects/new.html",{"account":account})



@login_required
def show(request, id):
    project = get_object_or_404(Project,id=id)
    account = request.user

    if request.POST:
        # 處理上架邏輯
        if "publish" in request.POST:  # 檢查是否點擊了上架按鈕
            if project.status == "pending":
                project.status = "live"  # 將狀態改為已上架
                project.start_at = timezone.now()  # 更新 start_at 為當前時間
                project.save()
                messages.success(request, "已上架")

                return redirect("projects:show", id=project.id)
        elif "unpublish" in request.POST:
            if project.status == "live":
                project.status = "ended"  # 將狀態改為已上架
                project.end_at = timezone.now()  # 更新 start_at 為當前時間
                project.save()
                messages.success(request, "已下架")

                return redirect("projects:show", id=project.id)

        else:
            form = ProjectFrom(request.POST, instance=project)
            form.save()
            return redirect("projects:show", id = project.id)

        return redirect("projects:show", id=project.id)

    collected = CollectProject.objects.filter(
        account=request.user, project=project
    ).first()

    collected = CollectProject.objects.filter(
        account=request.user, project=project
    ).first()

    favorited = project.favorite_users.filter(id=request.user.id).first()

    return render(
        request,
        "projects/show.html",
        {
            "project": project,
            "collected": collected,
            "account": account,
            "favorited": favorited,
        },
    )

@login_required
def edit(request, id):
    project = get_object_or_404(Project,id=id)
    format_time_start =localtime(project.start_at).strftime('%Y-%m-%dT%H:%M')
    format_time_end =localtime(project.end_at).strftime('%Y-%m-%dT%H:%M')
    return render(request, "projects/edit.html",{"project":project,
"format_time_start":format_time_start,"format_time_end":format_time_end})

@login_required
def delete(request, id):
    project = get_object_or_404(Project,id=id)
    if request.POST:
        project.delete()
        return redirect("projects:index")

    return render(
        request,
        "projects/delete.html",
    )


@login_required
@require_POST
def collect_projects(request, id):
    project = get_object_or_404(Project, id=id)
    collect, created = CollectProject.objects.get_or_create(
        account=request.user,
        project=project,
    )

    if not created:
        collect.delete()

    return redirect("projects:show", id=project.id)


@login_required
@require_POST
def like_projects(request, id):
    project = get_object_or_404(Project, id=id)
    favorite = project.favorite_users.filter(id=request.user.id).first()

    if favorite:
        FavoritePrject.objects.get(account=request.user, project=project).delete()
    else:
        FavoritePrject(account=request.user, project=project).save()

    return redirect("projects:show", id=project.id)
