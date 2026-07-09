import shutil
from pathlib import Path

ROOT = Path(__file__).parent

LANGUAGE_MAP = {
    ".py": "Python",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".c": "C",
    ".java": "Java",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".cs": "C#",
    ".go": "Go",
    ".rs": "Rust",
    ".rb": "Ruby",
    ".php": "PHP",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".scala": "Scala",
    ".sql": "SQL",
    ".mysql": "MySQL",
}

IGNORE = {
    ".md",
    ".txt",
    ".json",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
}

count = 0

folders = [f for f in ROOT.iterdir() if f.is_dir()]

for problem_folder in folders:

    if problem_folder.name in LANGUAGE_MAP.values():
        continue

    language = None

    for file in problem_folder.iterdir():

        if file.is_dir():
            continue

        ext = file.suffix.lower()

        if ext in IGNORE:
            continue

        if ext in LANGUAGE_MAP:
            language = LANGUAGE_MAP[ext]
            break

    if language is None:
        continue

    language_folder = ROOT / language
    language_folder.mkdir(exist_ok=True)

    destination = language_folder / problem_folder.name

    if destination.exists():
        print(f"Already exists: {problem_folder.name}")
        continue

    shutil.move(str(problem_folder), str(destination))
    print(f"Moved: {problem_folder.name} -> {language}")
    count += 1


# -------------------------------
# Update README links
# -------------------------------

readme = ROOT / "README.md"

if readme.exists():

    text = readme.read_text(encoding="utf-8")

    folder_map = {}

    # Build mapping from existing folders
    for language in LANGUAGE_MAP.values():

        language_path = ROOT / language

        if not language_path.exists():
            continue

        for folder in language_path.iterdir():

            if folder.is_dir():
                folder_map[folder.name] = f"{language}/{folder.name}"

    # Replace links
    for old_folder, new_folder in folder_map.items():

        text = text.replace(
            f"](./{old_folder}/)",
            f"](./{new_folder}/)"
        )

        text = text.replace(
            f"](./{old_folder})",
            f"](./{new_folder})"
        )

        text = text.replace(
            f"href=\"./{old_folder}/\"",
            f"href=\"./{new_folder}/\""
        )

    readme.write_text(text, encoding="utf-8")
