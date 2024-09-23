from django.db import models

# Create your models here.
class ScrapedData(models.Model):
    url = models.URLField(max_length=200)
    title = models.CharField(max_length=255)
    content = models.TextField()
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TextAnalysis(models.Model):
    scraped_data = models.OneToOneField(
        ScrapedData, on_delete=models.CASCADE, related_name="analysis"
    )
    sentiment = models.CharField(max_length=50)
    keywords = models.TextField()
    summary = models.TextField()
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis of {self.scraped_data.title}"
    
class AnalysisResult(models.Model):
    task = models.ForeignKey("Task", on_delete=models.CASCADE)
    analysis_type = models.CharField(max_length=255)
    result_data = models.TextField()
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis {self.analysis_type} for Task {self.task.id}"


class Task(models.Model):
    TASK_TYPE_CHOICES = (
        ("scraping", "Scraping"),
        ("analysis", "Analysis"),
    )
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )

    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    progress = models.IntegerField(default=0)  # Add progress field

    def __str__(self):
        return f"{self.task_type} - {self.status}"


class Log(models.Model):
    LOG_LEVEL_CHOICES = (
        ("info", "Info"),
        ("warning", "Warning"),
        ("error", "Error"),
    )

    timestamp = models.DateTimeField(auto_now_add=True)
    log_level = models.CharField(max_length=10, choices=LOG_LEVEL_CHOICES)
    message = models.TextField()

    def __str__(self):
        return f"[{self.timestamp}] {self.log_level.upper()}: {self.message}"


class Configuration(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()

    def __str__(self):
        return f"{self.key}: {self.value}"
