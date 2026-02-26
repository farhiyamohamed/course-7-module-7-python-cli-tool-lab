# lib/models.py
import json
import os

DATA_FILE = "tasks_data.json"

class Task:
    def __init__(self, title, completed=False):
        self.title = title
        self.completed = completed

    def complete(self):
        self.completed = True
        print(f"✅ Task '{self.title}' completed.")

    def to_dict(self):
        return {"title": self.title, "completed": self.completed}

    @staticmethod
    def from_dict(data):
        return Task(data["title"], data["completed"])


class User:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        print(f"📌 Task '{task.title}' added to {self.name}.")

    def list_tasks(self):
        if not self.tasks:
            print(f"ℹ️ {self.name} has no tasks.")
            return
        print(f"📋 Tasks for {self.name}:")
        for idx, task in enumerate(self.tasks, 1):
            status = "✔️" if task.completed else "❌"
            print(f"{idx}. [{status}] {task.title}")

    def get_task(self, title):
        for task in self.tasks:
            if task.title == title:
                return task
        return None

    def to_dict(self):
        return {"name": self.name, "tasks": [t.to_dict() for t in self.tasks]}

    @staticmethod
    def from_dict(data):
        user = User(data["name"])
        user.tasks = [Task.from_dict(t) for t in data["tasks"]]
        return user

# Load/save functions
def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
        return {u["name"]: User.from_dict(u) for u in data}

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump([u.to_dict() for u in users.values()], f, indent=2)