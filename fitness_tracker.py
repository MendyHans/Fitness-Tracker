"""Fitness Tracker Application

This script provides a command-line interface to manage workout routines,
track exercises, and set fitness goals using an SQLite database.
"""

import sqlite3

# Constant
DATABASE_FILE = "fitness_tracker.db"


# Connect to the SQLite database
def connect_db():
    """Connect to the SQLite database and return the connection and cursor."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    return conn, cursor


# Initialize the database
def initialize_db():
    """Create the database tables if they do not already exist."""
    conn, cursor = connect_db()

    # Create workout_categories table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS workout_categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT NOT NULL UNIQUE
    )
    """
    )

    # Create fitness_goals table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS fitness_goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        goal_name TEXT NOT NULL,
        target_value INTEGER NOT NULL,
        current_value INTEGER DEFAULT 0,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES workout_categories(id)
    )
    """
    )

    # Create exercises table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercise_name TEXT NOT NULL,
        muscle_group TEXT NOT NULL,
        reps INTEGER,
        sets INTEGER,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES workout_categories(id)
    )
    """
    )

    # Create workout_routines table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS workout_routines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        routine_name TEXT NOT NULL,
        exercise_ids TEXT NOT NULL  -- Stores comma-separated exercise IDs
    )
    """
    )

    # Commit changes and close the connection
    conn.commit()
    conn.close()


# Function to add a new exercise category
def add_exercise_category():
    """Add a new exercise category to the database."""
    category_name = input("Enter the name of the new exercise category: ")
    conn, cursor = connect_db()
    try:
        cursor.execute(
            "INSERT INTO workout_categories (category_name) VALUES (?)",
            (category_name,),
        )
        conn.commit()
        print(f"Exercise category '{category_name}' added successfully!")
    except sqlite3.IntegrityError:
        print(f"Exercise category '{category_name}' already exists.")
    finally:
        conn.close()


# Function to view exercises by category
def view_exercises_by_category():
    """View exercises in a specific category."""
    conn, cursor = connect_db()
    cursor.execute("SELECT id, category_name FROM workout_categories")
    categories = cursor.fetchall()
    if not categories:
        print("No exercise categories found.")
        return
    print("Exercise Categories:")
    for category in categories:
        print(f"{category[0]}. {category[1]}")
    category_id = input("Enter the category ID to view exercises: ")
    cursor.execute("SELECT * FROM exercises WHERE category_id = ?", (category_id,))
    exercises = cursor.fetchall()
    if not exercises:
        print("No exercises found in this category.")
    else:
        print(f"Exercises in Category {category_id}:")
        for exercise in exercises:
            print(
                f"""{exercise[0]}. {exercise[1]} ({exercise[2]})
                - {exercise[3]} reps x {exercise[4]} sets"""
            )
    conn.close()


# Function to delete an exercise category
def delete_exercise_category():
    """Delete an exercise category from the database."""
    category_id = input("Enter the ID of the exercise category to delete: ")
    conn, cursor = connect_db()
    cursor.execute("DELETE FROM workout_categories WHERE id = ?", (category_id,))
    if cursor.rowcount > 0:
        print(f"Exercise category with ID {category_id} deleted successfully!")
    else:
        print(f"No exercise category found with ID {category_id}.")
    conn.commit()
    conn.close()


# Function to create a workout routine
def create_workout_routine():
    """Create the workout routines from the exercises"""
    routine_name = input("Enter the name of the workout routine: ")
    exercise_ids = input("Enter the exercise IDs (comma-separated) for this routine: ")
    conn, cursor = connect_db()
    cursor.execute(
        "INSERT INTO workout_routines (routine_name, exercise_ids) VALUES (?, ?)",
        (routine_name, exercise_ids),
    )
    conn.commit()
    print(f"Workout routine '{routine_name}' created successfully!")
    conn.close()


# Function to view workout routines
def view_workout_routines():
    """View the current workout routines"""
    conn, cursor = connect_db()
    cursor.execute("SELECT * FROM workout_routines")
    routines = cursor.fetchall()
    if not routines:
        print("No workout routines found.")
    else:
        print("Workout Routines:")
        for routine in routines:
            print(f"{routine[0]}. {routine[1]} (Exercises: {routine[2]})")
    conn.close()


# Function to add a new exercise
def add_exercise():
    """Add a new exercise to a specific category."""
    conn, cursor = connect_db()

    # Display available categories
    cursor.execute("SELECT id, category_name FROM workout_categories")
    categories = cursor.fetchall()
    if not categories:
        print("No exercise categories found. Please add a category first.")
        return
    print("Available Categories:")
    for category in categories:
        print(f"{category[0]}. {category[1]}")

    # Get exercise details from the user
    category_id = input("Enter the category ID for the exercise: ")
    exercise_name = input("Enter the name of the exercise: ")
    muscle_group = input("Enter the muscle group targeted by the exercise: ")
    reps = int(input("Enter the number of reps: "))
    sets = int(input("Enter the number of sets: "))

    # Insert the exercise into the database
    cursor.execute(
        """
    INSERT INTO exercises (exercise_name, muscle_group, reps, sets, category_id)
    VALUES (?, ?, ?, ?, ?)
    """,
        (exercise_name, muscle_group, reps, sets, category_id),
    )

    conn.commit()
    print(f"Exercise '{exercise_name}' added successfully!")
    conn.close()


# Function to contribute towards fitness goals
def contribute_to_fitness_goal():
    """Update the progress of a fitness goal."""
    conn, cursor = connect_db()

    # Display available fitness goals
    cursor.execute(
        "SELECT id, goal_name, current_value, target_value FROM fitness_goals"
    )
    goals = cursor.fetchall()
    if not goals:
        print("No fitness goals found. Please set a fitness goal first.")
        return
    print("Available Fitness Goals:")
    for goal in goals:
        print(f"{goal[0]}. {goal[1]} (Current: {goal[2]}/{goal[3]})")

    # Get goal ID and contribution value from the user
    goal_id = input("Enter the ID of the fitness goal to contribute to: ")
    contribution = int(input("Enter the value to contribute: "))

    # Update the goal's current value
    cursor.execute(
        """
    UPDATE fitness_goals
    SET current_value = current_value + ?
    WHERE id = ?
    """,
        (contribution, goal_id),
    )

    conn.commit()
    print(f"Contribution of {contribution} added to goal ID {goal_id}!")
    conn.close()


# Function to view exercise progress
def view_exercise_progress():
    """View the progress of a fitness goal."""
    conn, cursor = connect_db()
    cursor.execute("SELECT * FROM fitness_goals")
    goals = cursor.fetchall()
    if not goals:
        print("No fitness goals found.")
    else:
        print("Exercise Progress:")
        for goal in goals:
            progress = (goal[3] / goal[2]) * 100
            print(f"{goal[0]}. {goal[1]}: {goal[3]}/{goal[2]} ({progress:.2f}%)")
    conn.close()


# Function to set fitness goals
def set_fitness_goals():
    """Create the fitness goals"""
    goal_name = input("Enter the name of the fitness goal: ")
    target_value = int(input("Enter the target value for this goal: "))
    category_id = input("Enter the category ID for this goal: ")

    conn, cursor = connect_db()
    cursor.execute(
        "INSERT INTO fitness_goals (goal_name, target_value, category_id) VALUES (?, ?, ?)",
        (goal_name, target_value, category_id),
    )
    conn.commit()
    print(f"Fitness goal '{goal_name}' added successfully!")
    conn.close()


# Function to view progress towards fitness goals
def view_progress_towards_fitness_goals():
    """view progress of a fitness goal"""
    conn, cursor = connect_db()
    cursor.execute(
        """
    SELECT fitness_goals.id, goal_name, target_value, current_value, category_name 
    FROM fitness_goals 
    JOIN workout_categories ON fitness_goals.category_id = workout_categories.id
    """
    )
    goals = cursor.fetchall()
    if not goals:
        print("No fitness goals found.")
    else:
        print("Progress Towards Fitness Goals:")
        for goal in goals:
            progress = (goal[3] / goal[2]) * 100
            print(
                f"{goal[0]}. {goal[1]} ({goal[4]}): {goal[3]}/{goal[2]} ({progress:.2f}%)"
            )
    conn.close()


# Main menu
def main_menu():
    """Display the main menu and handle user input."""
    while True:
        print("\nFitness Tracker Menu:")
        print("1. Add Exercise Category")
        print("2. View Exercise by Category")
        print("3. Delete Exercise by Category")
        print("4. Add Exercise")
        print("5. Create Workout Routine")
        print("6. View Workout Routine")
        print("7. View Exercise Progress")
        print("8. Set Fitness Goals")
        print("9. Contribute Towards Fitness Goals")
        print("10. View Progress Towards Fitness Goals")
        print("11. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_exercise_category()
        elif choice == "2":
            view_exercises_by_category()
        elif choice == "3":
            delete_exercise_category()
        elif choice == "4":
            add_exercise()
        elif choice == "5":
            create_workout_routine()
        elif choice == "6":
            view_workout_routines()
        elif choice == "7":
            view_exercise_progress()
        elif choice == "8":
            set_fitness_goals()
        elif choice == "9":
            contribute_to_fitness_goal()
        elif choice == "10":
            view_progress_towards_fitness_goals()
        elif choice == "11":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


# Run the program
if __name__ == "__main__":
    initialize_db()
    main_menu()
