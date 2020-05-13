
import json
import requests

#------------------------------------------------------------------------------

response = requests.get("https://jsonplaceholder.typicode.com/todos")
todos = json.loads(response.text)

"""
[
  ...
  {
     "userId": 10,
      "id": 200,
      "title": "ipsam aperiam voluptates qui",
      "completed": false
  },
  ...
]
"""

#------------------------------------------------------------------------------
# Define a function to filter out users with max completed TODOS.
# This function is applied via filter() to qualify each JSON record
# It leverages the global variable USERS


def keep(todo):
    is_complete = todo["completed"]
    has_max_count = str(todo["userId"]) in USERS
    return is_complete and has_max_count


#------------------------------------------------------------------------------

# Map of userId to number of complete TODOs for that user
todos_by_user = {}

# Increment complete TODOs count for each user.
for todo in todos:
    if todo["completed"]:
        try:
            # Increment the existing user's count.
            todos_by_user[todo["userId"]] += 1
        except KeyError:
            # This user has not been seen. Set their count to 1.
            todos_by_user[todo["userId"]] = 1

# Create a sorted list of (userId, num_complete) pairs.
top_users = sorted(todos_by_user.items(),
                   key=lambda x: x[1], reverse=True)
print("USERID,TODO_COUNT: ", top_users)

# Get the maximum number of complete TODOs.
max_complete = top_users[0][1]

# Create a list of all users who have completed the maximum number of TODOs.
USERS = []
for user, num_complete in top_users:
    if num_complete < max_complete:
        break
    USERS.append(str(user))

print(USERS)
max_users = " and ".join(USERS)


s = "s" if len(USERS) > 1 else ""
f = "user{s} {mu} completed {mc} TODOs"
print(f.format(s=s, mu=max_users, mc=max_complete))

#------------------------------------------------------------------------------

with open("filtered_todo.json", "w") as data_file:

    # apply the filter function to the imported JSON data, and write to disk
    filtered_todos = list(filter(keep, todos))
    json.dump(filtered_todos, data_file, indent=2)

