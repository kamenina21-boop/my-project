"""
目標管理・振り返りモジュール
目標の設定・進捗管理・定期的な振り返り
"""

import json
import os
from datetime import date


DATA_FILE = "data/goals.json"

STATUS_LABELS = {
    "active": "進行中",
    "completed": "達成",
    "paused": "一時停止",
    "cancelled": "中止"
}


def load_data():
    os.makedirs("data", exist_ok=True)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"goals": [], "next_id": 1, "reflections": []}


def save_data(data):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class GoalManager:
    def __init__(self):
        self.data = load_data()

    def _save(self):
        save_data(self.data)

    def add_goal(self):
        title = input("目標のタイトルを入力してください: ").strip()
        if not title:
            print("タイトルを入力してください。")
            return
        description = input("詳細・理由（任意）: ").strip()
        deadline = input("達成期限 (YYYY-MM-DD、任意): ").strip()
        print("カテゴリを選択してください:")
        print("1. 健康・運動  2. 勉強・スキル  3. 仕事・キャリア  4. 趣味  5. その他")
        cat_map = {"1": "健康・運動", "2": "勉強・スキル", "3": "仕事・キャリア", "4": "趣味", "5": "その他"}
        cat_choice = input("カテゴリ (1-5): ").strip()
        category = cat_map.get(cat_choice, "その他")

        goal = {
            "id": self.data["next_id"],
            "title": title,
            "description": description,
            "deadline": deadline if deadline else None,
            "category": category,
            "status": "active",
            "progress": 0,
            "created_at": date.today().isoformat(),
            "milestones": []
        }
        self.data["goals"].append(goal)
        self.data["next_id"] += 1
        self._save()
        print(f"目標「{title}」を設定しました！")

    def list_goals(self):
        goals = self.data["goals"]
        if not goals:
            print("目標が登録されていません。")
            return
        active = [g for g in goals if g["status"] == "active"]
        others = [g for g in goals if g["status"] != "active"]

        if active:
            print("\n--- 進行中の目標 ---")
            for goal in active:
                bar = "█" * (goal["progress"] // 10) + "░" * (10 - goal["progress"] // 10)
                deadline_str = f" [期限: {goal['deadline']}]" if goal["deadline"] else ""
                print(f"ID:{goal['id']} [{goal['category']}] {goal['title']}")
                print(f"   進捗: [{bar}] {goal['progress']}%{deadline_str}")

        if others:
            print("\n--- その他の目標 ---")
            for goal in others:
                status_label = STATUS_LABELS.get(goal["status"], goal["status"])
                print(f"ID:{goal['id']} [{status_label}] {goal['title']}")

    def update_progress(self):
        self.list_goals()
        if not self.data["goals"]:
            return
        try:
            goal_id = int(input("進捗を更新する目標のIDを入力してください: "))
        except ValueError:
            print("有効なIDを入力してください。")
            return
        goal = next((g for g in self.data["goals"] if g["id"] == goal_id), None)
        if not goal:
            print("目標が見つかりません。")
            return
        try:
            progress = int(input("現在の進捗 (0-100%): "))
            progress = max(0, min(100, progress))
        except ValueError:
            print("有効な数値を入力してください。")
            return
        goal["progress"] = progress
        if progress == 100:
            goal["status"] = "completed"
            goal["completed_at"] = date.today().isoformat()
            print(f"おめでとうございます！目標「{goal['title']}」を達成しました！")
        else:
            print(f"進捗を {progress}% に更新しました！")
        self._save()

    def add_milestone(self):
        self.list_goals()
        if not self.data["goals"]:
            return
        try:
            goal_id = int(input("マイルストーンを追加する目標のIDを入力してください: "))
        except ValueError:
            print("有効なIDを入力してください。")
            return
        goal = next((g for g in self.data["goals"] if g["id"] == goal_id), None)
        if not goal:
            print("目標が見つかりません。")
            return
        milestone = input("マイルストーンの内容: ").strip()
        if not milestone:
            return
        goal["milestones"].append({
            "content": milestone,
            "done": False,
            "created_at": date.today().isoformat()
        })
        self._save()
        print(f"マイルストーン「{milestone}」を追加しました！")

    def write_reflection(self):
        print("\n--- 振り返り ---")
        period = input("振り返り期間 (例: 今週、今月): ").strip() or "今週"
        print(f"【{period}の振り返り】")

        good = input("うまくいったこと: ").strip()
        bad = input("うまくいかなかったこと: ").strip()
        learned = input("学んだこと: ").strip()
        next_action = input("次のアクション: ").strip()
        motivation = input("モチベーション (1=低 〜 5=高): ").strip()

        reflection = {
            "date": date.today().isoformat(),
            "period": period,
            "good": good,
            "bad": bad,
            "learned": learned,
            "next_action": next_action,
            "motivation": motivation
        }
        self.data["reflections"].append(reflection)
        self._save()
        print("振り返りを保存しました！")

    def list_reflections(self):
        if not self.data.get("reflections"):
            print("振り返りがまだありません。")
            return
        print("\n--- 振り返り一覧 ---")
        for r in reversed(self.data["reflections"]):
            print(f"\n[{r['date']}] {r['period']}の振り返り")
            print(f"  よかったこと: {r.get('good', '')}")
            print(f"  課題: {r.get('bad', '')}")
            print(f"  学び: {r.get('learned', '')}")
            print(f"  次のアクション: {r.get('next_action', '')}")
            motivation = r.get("motivation", "")
            if motivation:
                stars = "★" * int(motivation) if motivation.isdigit() else motivation
                print(f"  モチベーション: {stars}")

    def menu(self):
        while True:
            print("\n--- 目標管理・振り返り ---")
            print("1. 目標を追加")
            print("2. 目標一覧・進捗確認")
            print("3. 進捗を更新")
            print("4. マイルストーンを追加")
            print("5. 振り返りを書く")
            print("6. 振り返り一覧")
            print("0. メインメニューに戻る")
            choice = input("選択: ").strip()
            if choice == "1":
                self.add_goal()
            elif choice == "2":
                self.list_goals()
            elif choice == "3":
                self.update_progress()
            elif choice == "4":
                self.add_milestone()
            elif choice == "5":
                self.write_reflection()
            elif choice == "6":
                self.list_reflections()
            elif choice == "0":
                break
            else:
                print("0〜6の数字を入力してください。")
