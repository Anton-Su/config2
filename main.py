import sys


def main():
    if len(sys.argv) != 3:
        print("Inctruction: python script.py <path_to_plantuml> <name_package>")
        sys.exit(1)


if __name__ == "__main__":
    main()