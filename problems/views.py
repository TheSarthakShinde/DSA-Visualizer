import os
from collections import OrderedDict

from django.conf import settings
from django.http import Http404
from django.shortcuts import render

PROBLEMS_DIR = os.path.join(settings.BASE_DIR, "problems", "templates", "problems")

# files here are never listed / rendered as a "problem"
EXCLUDE = {"base.html", "home.html", "_template.html"}

# order categories appear in on the homepage; anything not listed
# falls under "Other" at the end.
CATEGORY_ORDER = [
    "Arrays & Strings",
    "Two Pointers / Sliding Window",
    "Stack & Queue",
    "Linked List",
    "Trees & Tries",
    "Graphs",
    "Dynamic Programming",
    "Binary Search & Sorting",
    "Heaps / Backtracking",
    "Other",
]


def get_problems():
    """
    Scans problems/templates/problems/ and turns every .html file
    (except the excluded ones) into a problem entry.
    Optional metadata: put a first-line HTML comment in the file like
    <!-- difficulty: Easy | tags: array,hashmap | category: Arrays & Strings -->
    and it'll be picked up automatically.
    """
    problems = []
    if os.path.isdir(PROBLEMS_DIR):
        for fname in sorted(os.listdir(PROBLEMS_DIR)):
            if not fname.endswith(".html") or fname in EXCLUDE:
                continue
            slug = fname[:-5]
            title = slug.replace("_", " ").replace("-", " ").title()
            difficulty, tags, category = "", "", "Other"
            full_path = os.path.join(PROBLEMS_DIR, fname)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    head_lines = [f.readline() for _ in range(5)]
                meta_line = next(
                    (
                        ln
                        for ln in head_lines
                        if "difficulty:" in ln or "category:" in ln
                    ),
                    "",
                )
                if meta_line:
                    meta = meta_line.strip().strip("<!--").strip("-->").strip()
                    parts = [p.strip() for p in meta.split("|")]
                    for p in parts:
                        if p.startswith("difficulty:"):
                            difficulty = p.split(":", 1)[1].strip()
                        if p.startswith("tags:"):
                            tags = p.split(":", 1)[1].strip()
                        if p.startswith("category:"):
                            category = p.split(":", 1)[1].strip()
            except OSError:
                pass
            problems.append(
                {
                    "slug": slug,
                    "title": title,
                    "difficulty": difficulty,
                    "tags": tags,
                    "category": category,
                }
            )
    return problems


def get_grouped_problems():
    """Groups get_problems() output by category, in CATEGORY_ORDER."""
    problems = get_problems()
    buckets = {}
    for p in problems:
        buckets.setdefault(p["category"], []).append(p)

    grouped = OrderedDict()
    for cat in CATEGORY_ORDER:
        if cat in buckets:
            grouped[cat] = buckets.pop(cat)
    # any category not in CATEGORY_ORDER still shows up, appended at the end
    for cat, items in buckets.items():
        grouped[cat] = items
    return grouped


def home(request):
    return render(request, "problems/home.html", {"grouped": get_grouped_problems()})


def problem_detail(request, slug):
    full_path = os.path.join(PROBLEMS_DIR, f"{slug}.html")
    if not os.path.isfile(full_path):
        raise Http404("No such problem yet")
    return render(request, f"problems/{slug}.html", {"slug": slug})
