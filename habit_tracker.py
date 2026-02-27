"""
習慣トラッカーモジュール
習慣の記録・達成状況の確認・ストリーク管理
"""

import json
import os
from datetime import date, datetime, timedelta


DATA_FILE = "data/habits.json"


def load_data():
    os.makedirs("data", exist_ok=True)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"habits": [], "records": {}}


def save_data(data):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class HabitTracker:
    def __init__(self):
        self.data = load_data()

    def _save(self):
        save_data(self.data)

    def add_habit(self):
        name = input("習慣の名前を入力してください: ").strip()
        if not name:
            print("名前を入力してください。")
            return
        description = input("説明（任意）: ").strip()
        habit = {
            "id": len(self.data["habits"]) + 1,
            "name": name,
            "description": description,
            "created_at": date.today().isoformat()
        }
        self.data["habits"].append(habit)
        self._save()
        print(f"習慣「{name}」を追加しました！")

    def list_habits(self):
        if not self.data["habits"]:
            print("習慣が登録されていません。")
            return
        today = date.today().isoformat()
        records_today = self.data["records"].get(today, [])
        print("\n--- 登録済み習慣 ---")
        for habit in self.data["habits"]:
            done = "✓" if habit["id"] in records_today else "○"
            streak = self._calculate_streak(habit["id"])
            print(f"[{done}] ID:{habit['id']} {habit['name']} (連続 {streak} 日)")

    def complete_habit(self):
        self.list_habits()
        if not self.data["habits"]:
            return
        try:
            habit_id = int(input("達成した習慣のIDを入力してください: "))
        except ValueError:
            print("有効なIDを入力してください。")
            return

        today = date.today().isoformat()
        if today not in self.data["records"]:
            self.data["records"][today] = []

        if habit_id in self.data["records"][today]:
            print("この習慣は既に今日達成済みです！")
            return

        habit = next((h for h in self.data["habits"] if h["id"] == habit_id), None)
        if not habit:
            print("習慣が見つかりません。")
            return

        self.data["records"][today].append(habit_id)
        self._save()
        streak = self._calculate_streak(habit_id)
        print(f"習慣「{habit['name']}」を達成しました！現在 {streak} 日連続！")

    def _calculate_streak(self, habit_id):
        streak = 0
        check_date = date.today()
        while True:
            date_str = check_date.isoformat()
            if habit_id in self.data["records"].get(date_str, []):
                streak += 1
                check_date -= timedelta(days=1)
            else:
                break
        return streak

    def show_progress(self):
        if not self.data["habits"]:
            print("習慣が登録されていません。")
            return
        print("\n--- 過去7日間の達成状況 ---")
        dates = [(date.today() - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]
        header = "習慣名          " + " ".join(d[5:] for d in dates)
        print(header)
        print("-" * len(header))
        for habit in self.data["habits"]:
            row = f"{habit['name'][:14]:<16}"
            for d in dates:
                row += " ✓ " if habit["id"] in self.data["records"].get(d, []) else " ○ "
            print(row)

    def delete_habit(self):
        self.list_habits()
        if not self.data["habits"]:
            return
        try:
            habit_id = int(input("削除する習慣のIDを入力してください: "))
        except ValueError:
            print("有効なIDを入力してください。")
            return
        habit = next((h for h in self.data["habits"] if h["id"] == habit_id), None)
        if not habit:
            print("習慣が見つかりません。")
            return
        confirm = input(f"「{habit['name']}」を削除しますか？ (y/N): ")
        if confirm.lower() == "y":
            self.data["habits"].remove(habit)
            self._save()
            print(f"「{habit['name']}」を削除しました。")

    def menu(self):
        while True:
            print("\n--- 習慣トラッカー ---")
            print("1. 習慣を追加")
            print("2. 習慣一覧・今日の達成状況")
            print("3. 習慣を達成する")
            print("4. 週間進捗を表示")
            print("5. 習慣を削除")
            print("0. メインメニューに戻る")
            choice = input("選択: ").strip()
            if choice == "1":
                self.add_habit()
            elif choice == "2":
                self.list_habits()
            elif choice == "3":
                self.complete_habit()
            elif choice == "4":
                self.show_progress()
            elif choice == "5":
                self.delete_habit()
            elif choice == "0":
                break
            else:
                print("0〜5の数字を入力してください。")
