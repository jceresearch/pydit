""" Utility to generate a proposed changelog from git commit messages. 

"""

import subprocess
from datetime import datetime, timedelta
import pandas as pd

# Run the git log command to get the commit messages
result = subprocess.run(
    ["git", "log", "--pretty=format:%cd %s", "--date=format:%Y-%m-%d"],
    stdout=subprocess.PIPE,
    check=True,
)

# Decode the output from bytes to string
commit_messages = result.stdout.decode("utf-8")

# Split the string into a list of commit messages
commit_messages = commit_messages.split("\n")

commit_messages = [
    {
        "date": datetime.strptime(msg.split(" ")[0], "%Y-%m-%d"),
        "msg": " ".join(msg.split(" ")[1:]),
    }
    for msg in commit_messages
    if msg
]

recent_commits = [
    msg for msg in commit_messages if msg["date"] > datetime.now() - timedelta(days=90)
]

df = pd.DataFrame(recent_commits)
dfgrouped = df.groupby("date").agg({"msg": list})


# Write the commit messages to the CHANGELOG_AUTO.md file
with open("CHANGELOG_AUTO.md", "w", encoding="utf-8") as f:
    f.write("# Changelog\n\n")  # Write the header
    for cd, msgs in dfgrouped.iterrows():
        f.write(f"## {cd.strftime('%Y-%m-%d')}\n\n")
        for msg in msgs["msg"]:
            f.write(f"- {msg}\n")
        f.write("\n")
