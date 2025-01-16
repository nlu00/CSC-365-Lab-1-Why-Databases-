class Parser:
    """Parser class to handle user input dynamically."""
    def atEOF(self):
        """Check if the program should terminate."""
        return False

    def parse(self):
        """Get the next command from the user."""
        return input().strip()


class SchoolSearch:
    def __init__(self, header, prompt, parser, filename):
        self.header = header
        self.prompt = prompt
        self.parser = parser
        self.data = self.load_students(filename)

    def load_students(self, filename):
        """Load and parse students.txt into a list of dictionaries."""
        try:
            students = []
            with open(filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    students.append({
                        "StLastName": parts[0].strip(),
                        "StFirstName": parts[1].strip(),
                        "Grade": int(parts[2].strip()),
                        "Classroom": int(parts[3].strip()),
                        "Bus": int(parts[4].strip()),
                        "GPA": float(parts[5].strip()),
                        "TLastName": parts[6].strip(),
                        "TFirstName": parts[7].strip(),
                    })
            return students
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
            exit(1)
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            exit(1)

    def search(self):
        """Main search method."""
        self.printHeader()
        while True:
            self.printPrompt()
            command = self.parser.parse()
            try:
                self.processCommand(command)
            except Exception as e:
                print(f"Error: {e}")

    def processCommand(self, command):
        """Process a single command."""
        parts = command.strip().split()
        if not parts:
            raise ValueError("Missing command.")
        cmd = parts[0]
        params = parts[1:]

        if cmd == "S":
            self.handleStudent(params)
        elif cmd == "T":
            self.handleTeacher(params)
        elif cmd == "G":
            self.handleGrade(params)
        elif cmd == "B":
            self.handleBus(params)
        elif cmd == "A":
            self.handleAverage(params)
        elif cmd == "I":
            self.handleInfo()
        elif cmd == "Q":
            print("Exiting program.")
            exit(0)
        else:
            raise ValueError("Invalid command.")

    def handleStudent(self, params):
        """Handle S command."""
        if not params:
            raise ValueError("Missing student last name.")
        lastname = params[0].lower()  # Normalize input to lowercase
        include_bus = "B" in params  # Check if the "B" option is provided
        matches = [s for s in self.data if s["StLastName"].lower() == lastname]

        if not matches:
            print(f"No students found with last name: {params[0]}")
        else:
            for student in matches:
                if include_bus:
                    print(f"{student['StLastName']}, {student['StFirstName']}, Bus: {student['Bus']}")
                else:
                    print(f"{student['StLastName']}, {student['StFirstName']}, Grade: {student['Grade']}, "
                          f"Classroom: {student['Classroom']}, Teacher: {student['TLastName']}, {student['TFirstName']}")

    def handleTeacher(self, params):
        """Handle T command."""
        if not params:
            raise ValueError("Missing teacher last name.")
        lastname = params[0].lower()
        matches = [s for s in self.data if s["TLastName"].lower() == lastname]
        if not matches:
            print(f"No students found for teacher: {params[0]}")
        else:
            for student in matches:
                print(f"{student['StLastName']}, {student['StFirstName']}")

    def handleGrade(self, params):
        """Handle G command."""
        if not params:
            raise ValueError("Missing grade number.")
        try:
            grade = int(params[0])
            high_low = params[1] if len(params) > 1 else None
            matches = [s for s in self.data if s["Grade"] == grade]
            if not matches:
                print(f"No students found in grade: {grade}")
            elif high_low == "H":
                top_student = max(matches, key=lambda s: s["GPA"])
                print(f"{top_student['StLastName']}, {top_student['StFirstName']}, GPA: {top_student['GPA']}, "
                      f"Bus: {top_student['Bus']}, Teacher: {top_student['TLastName']}, {top_student['TFirstName']}")
            elif high_low == "L":
                lowest_student = min(matches, key=lambda s: s["GPA"])
                print(f"{lowest_student['StLastName']}, {lowest_student['StFirstName']}, GPA: {lowest_student['GPA']}, "
                      f"Bus: {lowest_student['Bus']}, Teacher: {lowest_student['TLastName']}, {lowest_student['TFirstName']}")
            else:
                for student in matches:
                    print(f"{student['StLastName']}, {student['StFirstName']}")
        except ValueError:
            print("Error: Invalid grade number.")

    def handleBus(self, params):
        """Handle B command."""
        if not params:
            raise ValueError("Missing bus route number.")
        try:
            bus = int(params[0])
            matches = [s for s in self.data if s["Bus"] == bus]
            if not matches:
                print(f"No students found on bus route: {bus}")
            else:
                for student in matches:
                    print(f"{student['StLastName']}, {student['StFirstName']}, Grade: {student['Grade']}, Classroom: {student['Classroom']}")
        except ValueError:
            print("Error: Invalid bus route number.")

    def handleAverage(self, params):
        """Handle A command."""
        if not params:
            raise ValueError("Missing grade number.")
        try:
            grade = int(params[0])
            matches = [s for s in self.data if s["Grade"] == grade]
            if not matches:
                print(f"No students found in grade: {grade}")
            else:
                avg_gpa = sum(s["GPA"] for s in matches) / len(matches)
                print(f"Grade {grade} Average GPA: {avg_gpa:.2f}")
        except ValueError:
            print("Error: Invalid grade number.")

    def handleInfo(self):
        """Handle I command."""
        counts = {}
        for student in self.data:
            counts[student["Grade"]] = counts.get(student["Grade"], 0) + 1
        for grade, count in sorted(counts.items()):
            print(f"Grade {grade}: {count} Students")

    def printHeader(self):
        """Print the header."""
        print(self.header)

    def printPrompt(self):
        """Print the prompt."""
        print(self.prompt, end='')


if __name__ == "__main__":
    # Initialize and run the SchoolSearch program
    parser = Parser()
    school_search = SchoolSearch(
        header="Welcome to SchoolSearch!\nTo exit, type 'Q'.",
        prompt="-> ",
        parser=parser,
        filename="students.txt"
    )
    school_search.search()

'''
import os
import sys

def load_students(filename):
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        sys.exit(1)
    students = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            student = {
                "StLastName": parts[0].strip(),
                "StFirstName": parts[1].strip(),
                "Grade": int(parts[2].strip()),
                "Classroom": int(parts[3].strip()),
                "Bus": int(parts[4].strip()),
                "GPA": float(parts[5].strip()),
                "TLastName": parts[6].strip(),
                "TFirstName": parts[7].strip(),
            }
            students.append(student)
    return students

def handle_student(params, students):
    if not params:
        print("Error: Missing student last name.")
        return
    lastname = params[0].lower()  
    bus = "B" in params
    matches = [s for s in students if s["StLastName"].lower() == lastname]  
    if not matches:
        print(f"No students found with last name: {params[0]}")
    else:
        for student in matches:
            if bus:
                print(f"{student['StLastName']}, {student['StFirstName']}, Bus: {student['Bus']}")
            else:
                print(f"{student['StLastName']}, {student['StFirstName']}, Grade: {student['Grade']}, "
                      f"Classroom: {student['Classroom']}, Teacher: {student['TLastName']}, {student['TFirstName']}")

def handle_teacher(params, students):
    if not params:
        print("Error: Missing teacher last name.")
        return
    lastname = params[0].lower()  
    matches = [s for s in students if s["TLastName"].lower() == lastname] 
    if not matches:
        print(f"No students found for teacher: {params[0]}")
    else:
        for student in matches:
            print(f"{student['StLastName']}, {student['StFirstName']}")

def handle_grade(params, students):
    if not params:
        print("Error: Missing grade number.")
        return
    try:
        grade = int(params[0])
        high_low = params[1] if len(params) > 1 else None
        matches = [s for s in students if s["Grade"] == grade]
        if not matches:
            print(f"No students found in grade: {grade}")
        elif high_low == "H":
            top_student = max(matches, key=lambda s: s["GPA"])
            print(f"{top_student['StLastName']}, {top_student['StFirstName']}, GPA: {top_student['GPA']}, "
                  f"Bus: {top_student['Bus']}, Teacher: {top_student['TLastName']}, {top_student['TFirstName']}")
        elif high_low == "L":
            lowest_student = min(matches, key=lambda s: s["GPA"])
            print(f"{lowest_student['StLastName']}, {lowest_student['StFirstName']}, GPA: {lowest_student['GPA']}, "
                  f"Bus: {lowest_student['Bus']}, Teacher: {lowest_student['TLastName']}, {lowest_student['TFirstName']}")
        else:
            for student in matches:
                print(f"{student['StLastName']}, {student['StFirstName']}")
    except ValueError:
        print("Error: Invalid grade number.")

def handle_bus(params, students):
    if not params:
        print("Error: Missing bus route number.")
        return
    try:
        bus = int(params[0])
        matches = [s for s in students if s["Bus"] == bus]
        if not matches:
            print(f"No students found on bus route: {bus}")
        else:
            for student in matches:
                print(f"{student['StLastName']}, {student['StFirstName']}, Grade: {student['Grade']}, Classroom: {student['Classroom']}")
    except ValueError:
        print("Error: Invalid bus route number.")

def handle_average(params, students):
    if not params:
        print("Error: Missing grade number.")
        return
    try:
        grade = int(params[0])
        matches = [s for s in students if s["Grade"] == grade]
        if not matches:
            print(f"No students found in grade: {grade}")
        else:
            avg_gpa = sum(s["GPA"] for s in matches) / len(matches)
            print(f"Grade {grade} Average GPA: {avg_gpa:.2f}")
    except ValueError:
        print("Error: Invalid grade number.")

def handle_info(students):
    grades = {i: 0 for i in range(7)}
    for student in students:
        grades[student["Grade"]] += 1
    for grade, count in grades.items():
        print(f"Grade {grade}: {count} Students")

def handle_command(command, students):
    cmd_parts = command.split()
    if not cmd_parts:
        print("Error: Missing command.")
        return
    cmd = cmd_parts[0]
    params = cmd_parts[1:]
    if cmd == "S":
        handle_student(params, students)
    elif cmd == "T":
        handle_teacher(params, students)
    elif cmd == "G":
        handle_grade(params, students)
    elif cmd == "B":
        handle_bus(params, students)
    elif cmd == "A":
        handle_average(params, students)
    elif cmd == "I":
        handle_info(students)
    elif cmd == "Q":
        print("Exiting program.")
        sys.exit(0)
    else:
        print("Invalid command. Try again.")

def main():
    students = load_students("students.txt")
    print("Welcome to schoolsearch!")
    while True:
        command = input("Enter command: ").strip()
        handle_command(command, students)

if __name__ == "__main__":
    main() 
    '''