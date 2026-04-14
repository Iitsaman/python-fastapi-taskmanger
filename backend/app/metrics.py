from prometheus_client import Counter
from prometheus_client import Gauge



users_registered = Counter("users_registered_total", "Total users registered")
user_logins = Counter("user_logins_total", "Total user logins")
tasks_created = Counter("tasks_created_total", "Total tasks created")
tasks_updated = Counter("tasks_updated_total", "Total tasks updated")
tasks_deleted = Counter("tasks_deleted_total", "Total tasks deleted")
failed_requests = Counter("failed_requests_total", "Total failed requests")
current_tasks = Gauge("current_tasks", "Current active tasks")