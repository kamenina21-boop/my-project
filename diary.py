"""
日記モジュール
日々の記録・気分・振り返りの管理
"""

import json
import os
from datetime import date


DATA_FILE = "data/diary.json"

MOOD_LABELS = {
    "1": "😊 最高",
    "2": "🙂 良い",
    "3": "😐 普通",
    "4": "😞 悪い",
    "5": "😢 最悪"
}


def load_data():
    os.makedirs("data", exist_ok=True)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"entries": {}}


def save_data(data):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class Diary:
    def __init__(self):
        self.data = load_data()

    def _save(self):
        save_data(self.data)

    def write_entry(self):
        today = date.today().isoformat()
        if today in self.data["entries"]:
            print(f"今日（{today}）の日記は既に書かれています。上書きしますか？")
            confirm = input("(y/N): ")
            if confirm.lower() != "y":
                return

        print("\n--- 気分を選択してください ---")
        for k, v in MOOD_LABELS.items():
            print(f"{k}. {v}")
        mood = input("気分 (1-5): ").strip()
        if mood not in MOOD_LABELS:
            mood = "3"

        print("今日の出来事・感想を書いてください（空行で入力完了）:")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        content = "\n".join(lines)

        print("今日のベストな出来事は？（任意）:")
        best = input().strip()

        print("明日に向けた一言（任意）:")
        tomorrow = input().strip()

        self.data["entries"][today] = {
            "mood": mood,
            "content": content,
            "best": best,
            "tomorrow": tomorrow
        }
        self._save()
        print(f"今日の日記を保存しました！({MOOD_LABELS[mood]})")

    def read_entry(self):
        date_str = input("日付を入力してください (YYYY-MM-DD、空白で今日): ").strip()
        if not date_str:
            date_str = date.today().isoformat()

        entry = self.data["entries"].get(date_str)
        if not entry:
            print(f"{date_str} の日記は見つかりません。")
            return

        print(f"\n--- {date_str} の日記 ---")
        print(f"気分: {MOOD_LABELS.get(entry['mood'], '不明')}")
        print(f"\n内容:\n{entry['content']}")
        if entry.get("best"):
            print(f"\n今日のベスト: {entry['best']}")
        if entry.get("tomorrow"):
            print(f"明日への一言: {entry['tomorrow']}")

    def list_entries(self):
        if not self.data["entries"]:
            print("日記がまだありません。")
            return
        print("\n--- 日記一覧 ---")
        for d in sorted(self.data["entries"].keys(), reverse=True):
            entry = self.data["entries"][d]
            mood_label = MOOD_LABELS.get(entry["mood"], "不明")
            preview = entry["content"][:30] + "..." if len(entry["content"]) > 30 else entry["content"]
            print(f"{d} [{mood_label}] {preview}")

    def show_mood_summary(self):
        if not self.data["entries"]:
            print("日記がまだありません。")
            return
        mood_counts = {k: 0 for k in MOOD_LABELS}
        for entry in self.data["entries"].values():
            mood = entry.get("mood", "3")
            if mood in mood_counts:
                mood_counts[mood] += 1

        print("\n--- 気分の統計 ---")
        total = sum(mood_counts.values())
        for k, label in MOOD_LABELS.items():
            count = mood_counts[k]
            bar = "■" * count
            print(f"{label}: {bar} ({count}日)")
        print(f"合計: {total}日分の日記")

    def menu(self):
        while True:
            print("\n--- 日記 ---")
            print("1. 今日の日記を書く")
            print("2. 日記を読む")
            print("3. 日記一覧")
            print("4. 気分の統計")
            print("0. メインメニューに戻る")
            choice = input("選択: ").strip()
            if choice == "1":
                self.write_entry()
            elif choice == "2":
                self.read_entry()
            elif choice == "3":
                self.list_entries()
            elif choice == "4":
                self.show_mood_summary()
            elif choice == "0":
                break
            else:
                print("0〜4の数字を入力してください。")
