from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from .models import *
import requests
from bs4 import BeautifulSoup
import json
import csv
from django. utils import timezone

# Create your views here.


# scraping
def start_scraping_task(request):
    if request.method == "POST":
        form = ScrapingForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["website_url"]
            depth = form.cleaned_data["scraping_depth"]
            keywords = form.cleaned_data["keywords"]

            # Create a new scraping task
            task = Task.objects.create(
                task_type="scraping",
                status="in_progress",
                result=f"Started scraping {url}",
                started_at=timezone.now(),  # Ensure the timestamp is set
            )

            print(f"Task created: {task}")  # Log the task creation
            # Fetch all tasks to see if they are being created at all
            all_tasks = Task.objects.all()
            print(all_tasks)

            # Check if tasks are being created with a different status
            pending_tasks = Task.objects.filter(status="pending")
            print(pending_tasks)

            completed_tasks = Task.objects.filter(status="completed")
            print(completed_tasks)

            failed_tasks = Task.objects.filter(status="failed")
            print(failed_tasks)

            # Start scraping in the background (this should ideally be done asynchronously)
            scrape_website(url, depth, keywords, task)

            return redirect("ongoing_scraping_tasks")
    else:
        form = ScrapingForm()

    return render(request, "scraping.html", {"form": form})


# def ongoing_scraping_tasks(request):
#     tasks = Task.objects.filter(task_type="scraping", status="in_progress")
#     print("Ongoing tasks:", tasks)
#     return render(request, "ongoing_tasks.html", {"tasks": tasks})
def download_data(request, task_id):
    # Fetch data related to the task
    task = get_object_or_404(Task, id=task_id)
    # results = ScrapedData.objects.filter(task=task)
    results = ScrapedData.objects.filter(url__icontains=task.result.split(" ")[-1])

    # Create an HTTP response with CSV content
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="scraped_data_{task_id}.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(["URL", "Title", "Content"])  # Header row
    for result in results:
        writer.writerow([result.url, result.title, result.content])

    return response


# def download_data(request, task_id):
#     # Get the data related to the task
#     data = ScrapedData.objects.filter(task_id=task_id)

#     # Create a CSV response
#     response = HttpResponse(content_type="text/csv")
#     response["Content-Disposition"] = (
#         f'attachment; filename="scraped_data_{task_id}.csv"'
#     )

#     writer = csv.writer(response)
#     writer.writerow(["URL", "Title", "Content"])

#     for item in data:
#         writer.writerow([item.url, item.title, item.content])

#     return response


def ongoing_scraping_tasks(request):
    ongoing_tasks = Task.objects.filter(task_type="scraping", status="in_progress")
    completed_tasks = Task.objects.filter(task_type="scraping", status="completed")
    return render(
        request,
        "ongoing_tasks.html",
        {"ongoing_tasks": ongoing_tasks, "completed_tasks": completed_tasks},
    )


def completed_scraping_tasks(request):
    tasks = Task.objects.filter(task_type="scraping", status="completed")
    return render(request, "completed_tasks.html", {"tasks": tasks})

from django.shortcuts import render, get_object_or_404
# def view_results(request, task_id):
#     task = get_object_or_404(Task, id=task_id)
#     # Assuming you have a related model `ScrapedData` for storing results
#     results = ScrapedData.objects.filter(task=task)
#     return render(request, "view_results.html", {"task": task, "results": results})


def view_results(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    # Adjust filtering logic as necessary
    results = ScrapedData.objects.filter(url__icontains=task.result.split(" ")[-1])

    return render(request, "view_results.html", {"results": results, "task": task})


def scrape_website(url, depth, keywords, task):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string if soup.title else "No title"
        content = soup.get_text()

        # Save scraped data
        ScrapedData.objects.create(url=url, title=title, content=content)

        # Update task status
        task.status = "completed"
        task.result = f"Successfully scraped {url}"
        task.completed_at = timezone.now()  # Ensure completed_at is set
        task.save()
    except Exception as e:
        task.status = "failed"
        task.result = str(e)
        task.save()
        Log.objects.create(log_level="error", message=str(e))


def settings(request):
    if request.method == "POST":
        form = SettingsForm(request.POST)
        if form.is_valid():
            frequency = form.cleaned_data["frequency"]
            user_agent = form.cleaned_data["user_agent"]
            rate_limit = form.cleaned_data["rate_limit"]

            # Save settings to Configuration model
            Configuration.objects.update_or_create(
                key="frequency", defaults={"value": frequency}
            )
            Configuration.objects.update_or_create(
                key="user_agent", defaults={"value": user_agent}
            )
            Configuration.objects.update_or_create(
                key="rate_limit", defaults={"value": rate_limit}
            )

            return redirect("settings")
    else:
        # Pre-fill form with current settings
        frequency = (
            Configuration.objects.filter(key="frequency").first().value or "daily"
        )
        user_agent = (
            Configuration.objects.filter(key="user_agent").first().value
            or "Mozilla/5.0"
        )
        rate_limit = (
            Configuration.objects.filter(key="rate_limit").first().value or "10"
        )
        form = SettingsForm(
            initial={
                "frequency": frequency,
                "user_agent": user_agent,
                "rate_limit": rate_limit,
            }
        )

    return render(request, "settings.html", {"form": form})


def analysis_view(request):
    return render(request, "analysis.html")


def start_analysis(request):
    if request.method == "POST":
        form = TextAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle the form submission
            return redirect(
                "analysis_results"
            )  # Or wherever you want to redirect after processing
    else:
        form = TextAnalysisForm()
    return render(request, "analysis.html", {"form": form})


def perform_analysis(request):
    if request.method == "POST":
        # Handle the analysis logic here
        # For example, process uploaded data, perform analysis, save results

        # Assuming you've done the analysis and stored the results
        analysis_result = TextAnalysis.objects.create(result="Sample Analysis Result")

        return redirect("analysis_results")  # Redirect to results page
    else:
        return HttpResponse("Invalid method", status=405)

def perform_analysis(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id")
        analysis_type = request.POST.get("analysis_type", "Keyword Extraction")

        # Get the task and ensure it exists
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            # Handle case where task doesn't exist
            return redirect("error_page")  # You could redirect to an error page

        # Placeholder for actual analysis logic
        result_data = (
            f"Example result data for {analysis_type}"  # Replace with actual logic
        )

        # Save the analysis result
        AnalysisResult.objects.create(
            task=task,
            analysis_type=analysis_type,
            result_data=result_data,
        )

        # Update the task status to 'completed'
        task.status = "completed"
        task.save()

        return redirect("analysis_results")  # Adjust with your actual results page view
    else:
        return redirect(
            "analysis_page"
        )  # Redirect to analysis page in case of non-POST requests


def analysis_results(request):
    results = AnalysisResult.objects.all()
    return render(request, "analysis_results.html", {"results": results})


def reports_view(request):
    return render(request, "reports.html")


def save_scraping_settings(request):
    # Logic to save scraping settings
    return HttpResponse('Save settings')

def error_page(request):
    return render(request, "error_page.html")


def help_view(request):
    return render(request, "help.html")


def profile_view(request):
    return render(request, "profile.html")


def logout_view(request):
    # Handle logout logic
    return render(request, "logout.html")


def dashboard(request):
    return render(request, "dashboard.html")


def pause_task(request, task_id):
    # Logic to pause the task
    task = Task.objects.get(id=task_id)
    task.status = "paused"  # Add 'paused' status to your choices if needed
    task.save()
    return redirect("ongoing_scraping_tasks")


# def pause_task(request, task_id):
#     task = get_object_or_404(Task, id=task_id)
#     if task.status == "in_progress":
#         task.status = "paused"  # Assuming you have a paused status or similar logic
#         task.save()
#     return redirect("ongoing_scraping_tasks")


def cancel_task(request, task_id):
    # Logic to cancel the task
    task = Task.objects.get(id=task_id)
    task.status = "cancelled"  
    return redirect("ongoing_scraping_tasks")
