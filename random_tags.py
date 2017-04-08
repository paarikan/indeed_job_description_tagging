import random

possible_tags = [
    "part-time-job",
    "full-time-job",
    "hourly-wage",
    "salary",
    "associate-needed",
    "bs-degree-needed",
    "ms-or-phd-needed",
    "licence-needed",
    "1-year-experience-needed",
    "2-4-years-experience-needed",
    "5-plus-years-experience-needed",
    "supervising-job"
]

print "tags"

for i in range(2921):
    print random.choice(possible_tags) + ' ' + random.choice(possible_tags)
