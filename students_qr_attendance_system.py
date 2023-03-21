from sys import argv
import attendance

def main(argv):
    if "--create" in argv:
        attendance.create_tables()
        print("TABLES CREATED.")

    if "--feed" in argv:
        attendance.feed()
        print("DUMMY DATA FED TO DB.")

    if "--file" in argv:
        # Read and insert to DB from next argument
        pass

    if "--scan" in argv:
        # Run camera scan stuff (must take a session_id)

        # test
        res = attendance.update_session_attendance(2, 7)
        if res == 1:
            print("you're not enrolled")
        elif res == 2:
            print("you're already in class")
        else:
            print("welcome to class!")
        #


if __name__ == "__main__":
    main(argv[1:])
