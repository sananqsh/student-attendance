from sys import argv
import attendance


# def update_student_state(id):
#   student = Student.find(id)
#
#   case(student.status):
#     when(""):
#
#     when(""):
#
#     when(""):
#
#     when(""):
#
#     else:


def main(argv):
    for arg in argv:
        if arg == "--create":
            attendance.create_tables()
            print("TABLES CREATED.")

        elif arg == "--feed":
            attendance.feed()
            print("DUMMY DATA FED TO DB.")

        elif arg == "--file":
            # Read and insert to DB from next argument
            pass


    # Run camera scan stuff


if __name__ == "__main__":
    main(argv[1:])
