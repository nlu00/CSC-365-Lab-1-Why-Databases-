class SchoolSearch:
    def __init__(self, header, prompt, filename):
        self.header = header
        self.prompt = prompt
        self.data = self.load_students(filename)

    def load_students(self, filename):
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
        self.print_header()
        while True:
            self.print_prompt()
            command = input().strip()
            try:
                self.process_command(command)
            except Exception as e:
                print(f"Error: {e}")

    def process_command(self, command):
        parts = command.strip().split()
        if not parts:
            raise ValueError("Missing command.")
        cmd = parts[0]
        params = parts[1:]

        if cmd == "S":
            self.handle_student(params)
        elif cmd == "T":
            self.handle_teacher(params)
        elif cmd == "G":
            self.handle_grade(params)
        elif cmd == "B":
            self.handle_bus(params)
        elif cmd == "A":
            self.handle_average(params)
        elif cmd == "I":
            self.handle_info()
        elif cmd == "Q":
            print("Exiting.")
            exit(0)
        else:
            raise ValueError("Invalid command.")

    def handle_student(self, params):
        if not params:
            raise ValueError("Missing student last name.")
        lastname = params[0].lower()  
        include_bus = "B" in params  
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

    def handle_teacher(self, params):
        if not params:
            raise ValueError("Missing teacher last name.")
        lastname = params[0].lower()
        matches = [s for s in self.data if s["TLastName"].lower() == lastname]
        if not matches:
            print(f"No students found for teacher: {params[0]}")
        else:
            for student in matches:
                print(f"{student['StLastName']}, {student['StFirstName']}")

    def handle_grade(self, params):
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
            print("Invalid grade number.")

    def handle_bus(self, params):
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

    def handle_average(self, params):
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
            print("Invalid grade number.")

    def handle_info(self):
        counts = {}
        for student in self.data:
            counts[student["Grade"]] = counts.get(student["Grade"], 0) + 1
        for grade, count in sorted(counts.items()):
            print(f"Grade {grade}: {count} Students")

    def print_header(self):
        print(self.header)

    def print_prompt(self):
        print(self.prompt, end='')


if __name__ == "__main__":
    school_search = SchoolSearch(
        header="Welcome to SchoolSearch!\nTo exit, type 'Q'.",
        prompt="-> ",
        filename="students.txt"
    )
    school_search.search()

