from django import template

register = template.Library()

@register.filter(name='filter_completed')
def filter_completed(tasks):
    """
    Filter and return only completed tasks
    Usage: {{ tasks|filter_completed }}
    """
    return tasks.filter(completed=True)

@register.filter(name='filter_pending')
def filter_pending(tasks):
    """
    Filter and return only pending (not completed) tasks
    Usage: {{ tasks|filter_pending }}
    """
    return tasks.filter(completed=False)

@register.filter(name='count_completed')
def count_completed(tasks):
    """
    Count completed tasks
    Usage: {{ tasks|count_completed }}
    """
    return tasks.filter(completed=True).count()

@register.filter(name='count_pending')
def count_pending(tasks):
    """
    Count pending tasks
    Usage: {{ tasks|count_pending }}
    """
    return tasks.filter(completed=False).count()

@register.filter(name='percentage_completed')
def percentage_completed(tasks):
    """
    Calculate the percentage of completed tasks
    Usage: {{ tasks|percentage_completed }}
    """
    total = tasks.count()
    if total == 0:
        return 0
    completed = tasks.filter(completed=True).count()
    return round((completed / total) * 100, 1)