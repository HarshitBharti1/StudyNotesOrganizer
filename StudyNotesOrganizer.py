
import json
from pathlib import Path
from datetime import datetime

# =====================================
# STUDY NOTES ORGANIZER
# =====================================

DATA_FILE = Path(__file__).parent / "study_notes.json"

SUBJECTS = [
    "Python",
    "Math",
    "Science",
    "History",
    "English",
    "Other"
]


def load_notes():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            print("Could not read notes file.")
    return []


def save_notes():
    DATA_FILE.write_text(
        json.dumps(notes, indent=4),
        encoding="utf-8"
    )


notes = load_notes()


def header():
    print("\n" + "=" * 45)
    print("          MY STUDY NOTES ORGANIZER")
    print("=" * 45)


def choose_subject():
    print("\nSUBJECTS")

    for i, subject in enumerate(SUBJECTS, 1):
        print(f"{i}. {subject}")

    choice = input("\nChoose subject: ")

    if choice.isdigit() and 1 <= int(choice) <= len(SUBJECTS):
        return SUBJECTS[int(choice) - 1]

    print("Invalid subject.")
    return None


def add_note():
    header()
    print("CREATE NEW NOTE")

    subject = choose_subject()

    if not subject:
        return

    title = input("\nNote title: ").strip()

    if not title:
        print("Title cannot be empty.")
        return

    print("\nWrite your note below.")
    print("Type END on a new line to finish.\n")

    lines = []

    while True:
        line = input()

        if line.strip() == "END":
            break

        lines.append(line)

    note = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "title": title,
        "subject": subject,
        "content": "\n".join(lines),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    notes.append(note)
    save_notes()

    print("\nNote saved successfully!")


def list_notes(filtered=None):
    results = notes if filtered is None else filtered

    if not results:
        print("\nNo notes found.")
        return

    for i, note in enumerate(results, 1):
        print(
            f"{i}. [{note['subject']}] "
            f"{note['title']} - {note['date']}"
        )


def view_notes():
    header()
    print("VIEW NOTES")

    subject = choose_subject()

    if not subject:
        return

    results = [
        note for note in notes
        if note["subject"] == subject
    ]

    list_notes(results)

    if not results:
        return

    choice = input("\nEnter note number to open (0 to go back): ")

    if choice == "0":
        return

    if choice.isdigit() and 1 <= int(choice) <= len(results):
        note = results[int(choice) - 1]

        print("\n" + "=" * 45)
        print("TITLE:", note["title"])
        print("SUBJECT:", note["subject"])
        print("DATE:", note["date"])
        print("-" * 45)
        print(note["content"])
        print("=" * 45)


def search_notes():
    header()
    print("SEARCH NOTES")

    keyword = input("\nSearch for: ").strip().lower()

    if not keyword:
        return

    results = [
        note for note in notes
        if keyword in note["title"].lower()
        or keyword in note["content"].lower()
        or keyword in note["subject"].lower()
    ]

    print(f"\nFound {len(results)} result(s):")
    list_notes(results)


def edit_note():
    header()
    print("EDIT NOTE")

    list_notes()

    if not notes:
        return

    choice = input("\nChoose note number: ")

    if not choice.isdigit() or not 1 <= int(choice) <= len(notes):
        print("Invalid choice.")
        return

    note = notes[int(choice) - 1]

    print("\nCurrent title:", note["title"])
    new_title = input("New title (Enter to keep): ").strip()

    if new_title:
        note["title"] = new_title

    print("\nCurrent content:")
    print(note["content"])

    print("\nEnter replacement content.")
    print("Type END on a new line to finish.")

    lines = []

    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    note["content"] = "\n".join(lines)
    note["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    save_notes()
    print("\nNote updated!")


def delete_note():
    header()
    print("DELETE NOTE")

    list_notes()

    if not notes:
        return

    choice = input("\nChoose note number: ")

    if not choice.isdigit() or not 1 <= int(choice) <= len(notes):
        print("Invalid choice.")
        return

    note = notes[int(choice) - 1]

    confirm = input(
        f"Delete '{note['title']}'? (y/n): "
    )

    if confirm.lower() == "y":
        notes.remove(note)
        save_notes()
        print("\nNote deleted!")
    else:
        print("\nCancelled.")


def dashboard():
    header()

    print("STUDY DASHBOARD")
    print("\nTotal notes:", len(notes))

    print("\nNotes by subject:")

    for subject in SUBJECTS:
        count = sum(
            1 for note in notes
            if note["subject"] == subject
        )

        print(f"{subject}: {count}")


def main():
    while True:
        header()

        print("1. Create a note")
        print("2. View notes")
        print("3. Search notes")
        print("4. Edit notes")
        print("5. Delete notes")
        print("6. Study dashboard")
        print("7. Exit")

        choice = input("\nSelect an option: ")

        if choice == "1":
            add_note()
        elif choice == "2":
            view_notes()
        elif choice == "3":
            search_notes()
        elif choice == "4":
            edit_note()
        elif choice == "5":
            delete_note()
        elif choice == "6":
            dashboard()
        elif choice == "7":
            print("\nYour notes have been saved. Goodbye!")
            break
        else:
            print("\nInvalid option!")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
