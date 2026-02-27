#!/usr/bin/env python3
"""
習慣トラッカー・生活管理アプリ
Habit Tracker, Todo List, Diary, Motivation & Goal Manager
"""

import sys
from habit_tracker import HabitTracker
from todo import TodoList
from diary import Diary
from goals import GoalManager


def print_menu():
    print("\n" + "="*40)
    print("  生活管理アプリ メインメニュー")
    print("="*40)
    print("1. 習慣トラッカー")
    print("2. Todoリスト")
    print("3. 日記")
    print("4. 目標管理・振り返り")
    print("0. 終了")
    print("="*40)


def main():
    habit_tracker = HabitTracker()
    todo_list = TodoList()
    diary = Diary()
    goal_manager = GoalManager()

    print("生活管理アプリへようこそ！")

    while True:
        print_menu()
        choice = input("選択してください: ").strip()

        if choice == "1":
            habit_tracker.menu()
        elif choice == "2":
            todo_list.menu()
        elif choice == "3":
            diary.menu()
        elif choice == "4":
            goal_manager.menu()
        elif choice == "0":
            print("アプリを終了します。お疲れ様でした！")
            sys.exit(0)
        else:
            print("無効な選択です。0〜4の数字を入力してください。")


if __name__ == "__main__":
    main()
