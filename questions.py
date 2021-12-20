####################################################

# POLL PROJECT QUESTION CUSTOMIZATION
# ERIC LI

####################################################

# Questions must be dictionaries containing:
#   prompt    the question posed to the user
#   type      the type of question

# Depending on the type, a question must also contain:
#   options   a list of options that will be shown to the user

# Changes to questions here will NOT show up unless data is cleared. Backups will be preserved.

# Accepted values for "type":
#   yn        yes or no
#   mc        multiple choice
#   mcms      multiple choice multiselect
#   writ      written answer

QUESTIONS = [
  {
    "prompt": "What's your name?",
    "type": "writ"
  },
  {
    "prompt": "Do you like coding club?",
    "type": "yn"
  },
  {
    "prompt": "What project would you like to do?",
    "type": "mc",
    "options": [
      "Machine Learning",
      "Web Dev",
      "Blockchain",
      "Competitive Programming",
      "Graphics/UI/UX Design",
      "Other"
    ]
  },
  {
    "prompt": "Any other projects you're interested in?",
    "type": "mcms",
    "options": [
      "Machine Learning",
      "Web Dev",
      "Blockchain",
      "Competitive Programming",
      "Graphics/UI/UX Design",
      "Other"
    ]
  }
]

# Add more code here to generate questions procedurally if you would like!

####################################################