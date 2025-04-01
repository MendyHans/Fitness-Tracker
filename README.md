Fitness Tracker App
Overview

The Fitness Tracker App is a Python-based command-line application designed to help users manage their fitness routines and track their progress towards fitness goals. The app allows users to:

    Add, view, and delete exercise categories.
    Add exercises to specific categories.
    Create and view workout routines.
    Set and track fitness goals.
    Contribute towards fitness goals and view progress.

Features

    Exercise Management:
        Add new exercise categories.
        Add exercises to categories with details like name, muscle group, reps, and sets.
        View exercises by category.
        Delete exercise categories.

    Workout Routines:
        Create custom workout routines by selecting exercises.
        View existing workout routines.

    Fitness Goals:
        Set fitness goals with a target value.
        Contribute towards fitness goals by updating progress.
        View progress towards fitness goals.

    Progress Tracking:
        View exercise progress and fitness goal progress.

Installation

Prerequisites:

    Python 3.x installed on your system.
    SQLite3 (usually comes pre-installed with Python).

Steps:

    Clone the repository or download the fitness_tracker.py file.
    Navigate to the project directory.
    Run the following command to start the app:

    python fitness_tracker.py

Usage

Main Menu:

    The app presents a menu with the following options:

    1. Add Exercise Category
    2. View Exercise by Category
    3. Delete Exercise by Category
    4. Add Exercise
    5. Create Workout Routine
    6. View Workout Routine
    7. View Exercise Progress
    8. Set Fitness Goals
    9. Contribute Towards Fitness Goals
    10. View Progress Towards Fitness Goals
    11. Quit

        Enter the number corresponding to the desired action.

    Adding Data:
        Follow the prompts to add exercise categories, exercises, workout routines, and fitness goals.

    Viewing Data:
        Use the appropriate menu options to view exercises, workout routines, and progress.

    Deleting Data:
        Use the "Delete Exercise by Category" option to remove a category and its associated exercises.

    Tracking Progress:
        Use the "Contribute Towards Fitness Goals" option to update your progress.
        Use the "View Progress Towards Fitness Goals" option to see your current progress.

Database Schema

The app uses an SQLite database (fitness_tracker.db) with the following tables:

    workout_categories: Stores exercise categories.
    exercises: Stores individual exercises linked to categories.
    fitness_goals: Stores fitness goals linked to categories.
    workout_routines: Stores workout routines with associated exercise IDs.

Example Workflow

    Add a new exercise category (e.g., "Cardio").
    Add exercises to the category (e.g., "Running", "Cycling").
    Create a workout routine using the exercises.
    Set a fitness goal (e.g., "Run 10 km").
    Contribute towards the goal (e.g., update progress after running 5 km).
    View progress towards the goal.
