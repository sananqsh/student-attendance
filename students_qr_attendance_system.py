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


def main():
    attendance.create_tables()
    attendance.feed()

if __name__ == "__main__":
    main()
