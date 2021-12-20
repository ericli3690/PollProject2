###############################################

# POLL PROJECT VERSION 2
# ver 1.0
# ERIC LI

###############################################

# Hello, developer.
# Use the below toggle to enable administrative permissions.
ADMIN_MODE_ON = True
# Or, go to questions.py in the navigation hierarchy to customize the questions posed to the user.
# Note: changes to questions will not take effect until data is cleared via admin action 3

###############################################

print("IMPORTING LIBRARIES...")

from questions import QUESTIONS

# libs
# this script relies heavily on terminal_package.ask()
from terminal_package import color_print, ask
from os import system
from replit import db
from datetime import datetime
from collections import Counter

# user friendly poll
def main():
  # clear console, print greeting
  system("clear")
  color_print("SWC Coding Club Poll - Eric Li", "cyan")

  if not db.get("DATA"):
    # if ran for the first time or data was just cleared, create database
    db["DATA"] = QUESTIONS
    for question in db["DATA"]:
      question["answers"] = []

  if not db.get("BACKUPS"):
    # if ran for the first time or backups were just cleared, create backups
    db["BACKUPS"] = []

  for i, question in enumerate(db["DATA"]):
    # for each question in questions.py
    # print prompt
    color_print(question["prompt"], "blue")

    # if question is yes or no
    if question["type"] == "yn":
      color_print("Please type 'y' for yes, or 'n' for no.", "cyan")
      # check if filter is yes or no
      def yn_filter(reply):
        if reply == "y" or reply == "n":
          return True, "Accepted."
        else:
          return False, "Please enter either 'y' or 'n'."
      # append the answer to data.currentQuestion.answers
      db["DATA"][i]["answers"].append(
        ask(">>> ", yn_filter)
      )

    # if question is written response
    elif question["type"] == "writ":
      color_print("Please type your answer.", "cyan")
      def writ_filter(reply):
        return True, "Accepted."
      db["DATA"][i]["answers"].append(
        ask(">>> ", writ_filter)
      )

    # if question is multiple choice, single answer
    elif question["type"] == "mc":
      color_print("Please type one of the below numbers.", "cyan")
      # print each option out with an index for the user to type
      for j, option in enumerate(question["options"]):
        color_print(
          f"[{j + 1}]: {option}",
          "blue"
        )
      # the number of options
      num_of_options = len(question["options"])
      # filter to make sure only permitted values are typed in
      def mc_filter(reply):
        try:
          # must be a number
          int(reply)
        except ValueError:
          return False, "Please enter a number."
        if int(reply) in list(range(1, num_of_options + 1)):
          # is within the options of the question
          return True, "Accepted."
        else:
          return False, "This is not an option."
      db["DATA"][i]["answers"].append(
        ask(">>> ", mc_filter)
      )

    # if the question is multiple choice, multiple answer
    elif question["type"] == "mcms":
      color_print("Please type however many of the below numbers you would like to select, separated by commas.", "cyan")
      for j, option in enumerate(question["options"]):
        color_print(
          f"[{j + 1}]: {option}",
          "blue"
        )
      num_of_options = len(question["options"])
      def mcms_filter(reply):
        # split the user input to create a list
        selections = reply.replace(" ", "").split(",")
        # already picked selections, to evaluate against later selections in the list
        picked_selections = []
        for j, selection in enumerate(selections):
          try:
            int(selection)
          except ValueError:
            return False, "Please enter numbers separated by commas."
          if int(selection) in list(range(1, num_of_options + 1)):
            if selection not in picked_selections:
              # if this value has not been used before
              picked_selections.append(selection)
              # this value made it through all tests, onto the next one
              continue
            else:
              return False, f"{selection} was entered multiple times."
          else:
            return False, f"{selection} is not an option."
        # all values made it through all tests
        return True, "Accepted."
      db["DATA"][i]["answers"].append(
        # take the raw string and split it apart like before
        ask(">>> ", mcms_filter).replace(" ", "").split(",")
      )
    
    else:
      # someone using questions.py filled in an invalid type
      raise ValueError("INVALID QUESTION IN POLL SETTINGS")
  
  color_print("\nThank you for submitting your answer!", "cyan")

  # make a backup with a timestamp, append to a list at database.backups
  current_timestamp = str(datetime.now())
  db["BACKUPS"].append(
    {
      "timestamp": current_timestamp,
      "DATA": db["DATA"]
    }
  )

  color_print("Press ENTER to submit another entry, or type anything else to quit.", "cyan")
  
  if input(">>> "):
    # typed nothing, quit the program
    pass
  else:
    # clear, reset, replay
    system("clear")
    main()

# when admin settings are on, run this instead of main
def admin():

  # filter to make sure user input is a number from 1 to 6, used for admin console navigation
  def actions_filter(reply):
    try:
      # check if reply is number
      int(reply)
    except ValueError:
      return False, "Please enter a number."
    if int(reply) in list(range(1, 7)):
      # check if reply is between 1 and 7
      return True, "Accepted."
    else:
      return False, "Please enter a value from 1 to 6."

  # formats a database entry into legible text
  def format_data(data):
    # a database is made of answers for each question
    # for each question:
    for i, question in enumerate(data):
      # print the basic info about the question, ex the question index in the database (ie order its proposed to the user), the prompt posed, the type of question, etc.
      print(f"QUESTION {i + 1}")
      print(f"Prompt: {question['prompt']}")
      print(f"Type: {question['type']}")
      # if its a multiple choice question, there are also options that the user can choose from, print those
      if question["type"] == "mc" or question["type"] == "mcms":
        print(f"Options: {list(question['options'])}")

      # printing the answers collected by the poll
      print("Answers:")
      if question["type"] == "mcms":
        # multiple choice multiple answer question answers are formatted as lists, format those properly as lists instead of a funky database type
        for answer in question["answers"]:
          print(list(answer))
      else:
        # else just print them straight out
        for answer in question["answers"]:
          print(answer)

      # print instances of answers; for example, yes and no questions are printed as before to ensure a line graph could be drawn, but the amount of 'yes' and 'no' also matters; thus print them out using collections.Counter
      print("Total Counts:")
      if question["type"] == "mcms":
        # this data is made of multiple smaller lists, remove those containers and dump all the data into one massive array
        aggregate_data = []
        for answer in question["answers"]:
          for data_point in answer:
            aggregate_data.append(data_point)
        # pass that massive array to collections.Counter, which will tally the instances of all elements up, then convert it to a dictionary and print it
        print(dict(Counter(aggregate_data)))
      else:
        # else just print collections.Counter's operation on them as a dictionary
        print(dict(Counter(question["answers"])))
      # whitespace
      print()

  # the console
  while True:
    # while True to redraw it after each action, clear and colorprint title
    system('clear')
    color_print("SWC Coding Club Poll - Eric Li - ADMIN MODE", "red")

    # visual
    color_print(
      "Type '1' to view all data."
      "\nType '2' to view all backups."
      "\nType '3' to clear all data."
      "\nType '4' to clear all backups."
      "\nType '5' to exit admin mode and fill out the form."
      "\nType '6' to quit."
      "\nNote that any deletions are permanent.",
      "red"
    )
    action = ask(">>> ", actions_filter)

    # conditional check
    if action == "1":
      color_print("\nLOADING...\n", "cyan")
      if db.get("DATA"):
        format_data(db["DATA"])
      else:
        # data was just cleared or is empty
        color_print("DATA is empty.", "red")
    elif action == "2":
      color_print("\nLOADING...\n", "cyan")
      if db.get("BACKUPS"):
        # for each backup in the backups "folder"
        for i, backup in enumerate(db["BACKUPS"]):
          # print its timestamp
          print(f"--- BACKUP {i + 1} : {backup['timestamp']} ---")
          # format
          format_data(backup["DATA"])
          # whitespace separators
          print("\n\n\n\n")
      else:
        # backups was just cleared or is empty
        color_print("BACKUPS are empty.", "red")
    elif action == "3":
      # None is what it returns if it was already cleared previously
      db.pop("DATA", None)
      color_print("Data cleared.", "red")
    elif action == "4":
      # None is what it returns if it was already cleared previously
      db.pop("BACKUPS", None)
      color_print("Backups cleared.", "red")
    elif action == "5":
      # clear and begin a nested instance of main that returns here after finishing
      system('clear')
      main()
    elif action == "6":
      # exit
      break

    # return to console
    color_print("Press ENTER to return to the admin console.", "red")
    input(">>> ")

# run main or admin
if ADMIN_MODE_ON:
  admin()
else:
  main()