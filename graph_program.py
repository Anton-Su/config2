import sys
import os
import subprocess

path_to_spisok_package = os.getcwd() + "\\dependencies.txt"
dependencies = {}
output_name = "vremen"


def showing_pic(name):
    path_picture = os.getcwd() + "\\" + name
    if not os.path.exists(path_picture):
        print("picture not found")
        return False
    if os.name == "nt":  # windows
        subprocess.run(["start", path_picture], shell=True)
    else:  # unix
        subprocess.run(["xdg-open", path_picture])
    return True


def render_plantuml_file(uml_text, path_to_uml):
    with open(f"{output_name}.puml", "w") as f:
        f.write(uml_text)
    try:
        subprocess.run(["java", "-jar", path_to_uml, f"{output_name}.puml"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print("Ошибка при запуске PlantUML:", e)
    return False


def transform_to_uml_format():
    itog = ''
    for package, deps in dependencies.items():
        for dep in deps:
            itog += f"{package} --> {dep}\n"
    return itog


def detect_dependencies_recur(file_path):
    current_dependence = ""
    with open(file_path, "r") as f:
        for line in f:
            stroka = line.strip()
            if not stroka:
                continue
            if not stroka.startswith("Depends:"):
                current_dependence = stroka
                dependencies[current_dependence] = []
            else:
                dependencies[current_dependence].append(stroka.split(": ")[1])
    return dependencies


def get_dependencies(package_name):
    result = subprocess.run(
        ["apt-cache", "depends", package_name], capture_output=True,
        text=True, check=True)
    with open(f"{output_name}.txt", "w") as file:
        file.write(result.stdout)
    return 1


def main(package_name, path_uml):
    if not os.path.exists(path_uml) or not os.path.exists(path_to_spisok_package):
        print('os error')
        return
    # get_dependencies(package_name)
    detect_dependencies_recur(path_to_spisok_package)
    itog = transform_to_uml_format()
    if len(itog) > 0:
        render_plantuml_file("@startuml\n" + itog + "@enduml\n", path_uml)
        showing_pic(f"{output_name}.png")
    else:
        print("такого пакета не нашлось")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Аргументы указаны неверно")
        exit()
    path_uml = sys.argv[1]
    package_name = sys.argv[2]
    main(package_name, path_uml)