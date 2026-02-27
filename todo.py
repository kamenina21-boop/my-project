"""
Todoリストモジュール
タスクの追加・完了・削除・優先度管理
"""

import json
import os
from datetime import date


DATA_FILE = "data/todos.json"


def load_data():
    os.makedirs("data", exist_ok=True)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"todos": [], "next_id": 1}


def save_data(data):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


PRIORITY_LABELS = {"1": "高", "2": "中", "3": "低"}


class TodoList:
    def __init__(self):
        self.data = load_data()

    def _save(self):
        save_data(self.data)

    def add_todo(self):
        title = input("タスク名を入力してください: ").strip()
        if not title:
            print("タスク名を入力してください。")
            return
        print("優先度を選択してください: 1=高 2=中 3=低")
        priority = input("優先度 (デフォルト: 2): ").strip() or "2"
        if priority not in PRIORITY_LABELS:
            priority = "2"
        due = input("期限 (YYYY-MM-DD、任意): ").strip()

        todo = {
            "id": self.data["next_id"],
            "title": title,
            "priority": priority,
            "due": due if due else None,
            "done": False,
            "created_at": date.today().isoformat()
        }
        self.data["todos"].append(todo)
        self.data["next_id"] += 1
        self._save()
        print(f"タスク「{title}」を追加しました！")

    def list_todos(self, show_done=False):
        todos = self.data["todos"]
        if not show_done:
            todos = [t for t in todos if not t["done"]]
        if not todos:
            print("タスクがありません。" if show_done else "未完了のタスクがありません。")
            return
        # 優先度でソート
        todos = sorted(todos, key=lambda t: t["priority"])
        print("\n--- Todoリスト ---")
        for todo in todos:
            status = "✓" if todo["done"] else "○"
            priority_label = PRIORITY_LABELS.get(todo["priority"], "中")
            due_str = f" [期限: {todo['due']}]" if todo["due"] else ""
            print(f"[{status}] ID:{todo['id']} [{priority_label}] {todo['title']}{due_str}")

    def complete_todo(self):
        self.list_todos()
        try:
            todo_id = int(input("完了するタスクのIDを入力してください: "))
        except ValueError:
            print("有効なIDを入力してください。")
            return
        todo = next((t for t in self.data["todos"] if t["id"] == todo_id), None)
        if not todo:
            print("タスクが見つかりません。")
            return
        if todo["done"]:
            print("このタスクは既に完了しています。")
            return
        todo["done"] = True
        todo["completed_at"] = date.today().isoformat()
        self._save()
        print(f"タスク「{todo['title']}」を完了しました！")

    def delete_todo(self):
        self.list_todos(show_done=True)
        try:
            todo_id = int(input("削除するタスクのIDを入力してください: "))
        except ValueError:
            print("有効なIDを入力してください。")
            return
        todo = next((t for t in self.data["todos"] if t["id"] == todo_id), None)
        if not todo:
            print("タスクが見つかりません。")
            return
        confirm = input(f"「{todo['title']}」を削除しますか？ (y/N): ")
        if confirm.lower() == "y":
            self.data["todos"].remove(todo)
            self._save()
            print(f"「{todo['title']}」を削除しました。")

    def menu(self):
        while True:
            print("\n--- Todoリスト ---")
            print("1. タスクを追加")
            print("2. 未完了タスク一覧")
            print("3. 全タスク一覧")
            print("4. タスクを完了にする")
            print("5. タスクを削除")
            print("0. メインメニューに戻る")
            choice = input("選択: ").strip()
            if choice == "1":
                self.add_todo()
            elif choice == "2":
                self.list_todos()
            elif choice == "3":
                self.list_todos(show_done=True)
            elif choice == "4":
                self.complete_todo()
            elif choice == "5":
                self.delete_todo()
            elif choice == "0":
                break
            else:
                print("0〜5の数字を入力してください。")
