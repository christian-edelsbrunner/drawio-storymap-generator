import yaml
import random


def generate_huge_map():
    swimlanes = ["MVP", "Release 1.1", "Release 1.2", "Backlog"]
    statuses = ["To Do", "In Progress", "Done"]

    epic_counter = 1

    goals = []
    for g in range(1, 6):
        features = []
        for f in range(1, 11):
            epics = []
            num_epics = random.randint(2, 5)
            for e in range(num_epics):
                epic_id = f"PROJ-{epic_counter}"
                epic_counter += 1

                epics.append(
                    {
                        "id": epic_id,
                        "title": f"Epic {epic_id} for Feature {f}",
                        "status": random.choice(statuses),
                        "url": f"https://jira.company.com/browse/{epic_id}",
                        "release": random.choice(
                            swimlanes[: random.randint(1, 3)]
                        ),  # Pick from 1 to 3 swimlanes
                    }
                )

            features.append(
                {
                    "id": f"FEAT-{g}-{f}",
                    "title": f"Feature {g}.{f}",
                    "status": random.choice(statuses),
                    "epics": epics,
                }
            )

        goals.append({"id": f"GOAL-{g}", "title": f"Goal {g}", "features": features})

    data = {
        "maps": [
            {
                "id": "MAP-1",
                "title": "Huge Enterprise Project",
                "releases": swimlanes,
                "goals": goals,
            }
        ]
    }

    with open("huge_map.yaml", "w") as f:
        yaml.dump(data, f, sort_keys=False, default_flow_style=False)


if __name__ == "__main__":
    generate_huge_map()
