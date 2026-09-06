from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Report
from .forms import ReportForm, SearchFilterForm

def home(request):
    recent_reports = Report.objects.order_by('-created_at')[:5]
    return render(request, 'home.html', {'recent_reports': recent_reports})

def report_list(request):
    reports = Report.objects.all().order_by('-created_at')
    form = SearchFilterForm(request.GET)

    if form.is_valid():
        if form.cleaned_data.get('search'):
            reports = reports.filter(item_name__icontains=form.cleaned_data['search'])
        if form.cleaned_data.get('type'):
            reports = reports.filter(type=form.cleaned_data['type'])
        if form.cleaned_data.get('category'):
            reports = reports.filter(category__icontains=form.cleaned_data['category'])
        if form.cleaned_data.get('status'):
            reports = reports.filter(status=form.cleaned_data['status'])

    return render(request, 'reports.html', {'reports': reports, 'form': form})

def report_detail(request, id):
    report = get_object_or_404(Report, id=id)
    return render(request, 'report_detail.html', {'report': report})

def report_create(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report created successfully!')
            return redirect('report_list')
    else:
        form = ReportForm()
    return render(request, 'report_form.html', {'form': form, 'title': 'Create Report'})

def report_update(request, id):
    report = get_object_or_404(Report, id=id)
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report updated successfully!')
            return redirect('report_detail', id=report.id)
    else:
        form = ReportForm(instance=report)
    return render(request, 'report_form.html', {'form': form, 'title': 'Edit Report'})

def report_delete(request, id):
    report = get_object_or_404(Report, id=id)
    if request.method == 'POST':
        report.delete()
        messages.success(request, 'Report deleted successfully!')
        return redirect('report_list')
    return render(request, 'report_confirm_delete.html', {'report': report})

def mark_resolved(request, id):
    report = get_object_or_404(Report, id=id)
    report.status = 'Resolved'
    report.save()
    messages.success(request, 'Report marked as resolved!')
    return redirect('report_detail', id=report.id)