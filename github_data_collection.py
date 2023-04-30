import csv
from typing import List
from github import Github
from datetime import datetime

ACCESS_TOKEN = "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"

# Initialize GitHub object
g = Github(ACCESS_TOKEN)

# Search repositories function
def search_repos(query: str, min_stars: int, min_commits: int) -> List[str]:
    repos = g.search_repositories(query=f"{query} in:description in:readme stars:>{min_stars} size:>{min_commits}")
    return [repo.full_name for repo in repos[:20]]

# Fetch commits function
def fetch_commits(repo_name: str, keywords: List[str]) -> List[dict]:
    repo = g.get_repo(repo_name)
    
    all_commits = repo.get_commits(since=datetime.fromisoformat("2022-05-01T00:00:00Z".replace("Z", "+00:00")))
    filtered_commits = []
    
    for commit in all_commits:
        message = commit.commit.message.lower()
        if any(keyword.lower() in message for keyword in keywords):
            filtered_commits.append({"repo": repo_name, "sha": commit.sha, "message": commit.commit.message})
    
    return filtered_commits

# Parameters for the search
query = "cuda+openmp"
min_stars = 100
min_commits = 1000
keywords = ["performance", "speed up", "accelerate", "fast", "slow", "latency", "contention", "optimize", "efficient"]

# Search for repositories and fetch relevant commits
repo_names = search_repos(query, min_stars, min_commits)
all_commits = []
for repo_name in repo_names:
    commits = fetch_commits(repo_name, keywords)
    all_commits.extend(commits)

# Write the results to a CSV file
with open("commits.csv", "w", newline="") as csvfile:
    fieldnames = ["repo", "sha", "message"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for commit in all_commits:
        writer.writerow(commit)


