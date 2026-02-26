# cli_tool.py
import argparse
from lib.models import Task, User, load_users, save_users

users = load_users()

def add_task(args):
    user = users.get(args.user) or User(args.user)
    users[args.user] = user
    task = Task(args.title)
    user.add_task(task)
    save_users(users)

def complete_task(args):
    user = users.get(args.user)
    if user:
        task = user.get_task(args.title)
        if task:
            task.complete()
            save_users(users)
        else:
            print("❌ Task not found.")
    else:
        print("❌ User not found.")

def list_tasks(args):
    user = users.get(args.user)
    if user:
        user.list_tasks()
    else:
        print("❌ User not found.")

def main():
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Add task
    add_parser = subparsers.add_parser("add-task", help="Add a new task")
    add_parser.add_argument("user")
    add_parser.add_argument("title")
    add_parser.set_defaults(func=add_task)

    # Complete task
    complete_parser = subparsers.add_parser("complete-task", help="Complete a task")
    complete_parser.add_argument("user")
    complete_parser.add_argument("title")
    complete_parser.set_defaults(func=complete_task)

    # List tasks
    list_parser = subparsers.add_parser("list-tasks", help="List all tasks for a user")
    list_parser.add_argument("user")
    list_parser.set_defaults(func=list_tasks)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()