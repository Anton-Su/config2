import sys
import os
import subprocess

path_to_name_package = os.getcwd() + "\\dependencies.txt"
dependencies = {}


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
    with open("vremen.puml", "w") as f:
        f.write(uml_text)
    try:
        subprocess.run(["java", "-jar", path_to_uml, "vremen.puml"], check=True)
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


def detect_dependencies_recur(file_path, name_package):
    flag = False
    with open(file_path, "r") as f:
        for line in f:
            stroka = line.strip()
            if stroka == name_package:
                 dependencies[name_package] = []
                 flag = True
            elif flag and not stroka.startswith("Depends:"):
                break
            elif flag:
                dependencies[name_package].append(stroka.split(": ")[1])
    if flag:
        for i in dependencies[name_package]:
            if i not in dependencies:
                detect_dependencies_recur(file_path, i)
    return dependencies


def main(package_name, path_uml):
    if not os.path.exists(path_uml) or not os.path.exists(path_to_name_package):
        print('os error')
        return
    detect_dependencies_recur(path_to_name_package, package_name)
    itog = transform_to_uml_format()
    if len(itog) > 0:
        render_plantuml_file("@startuml\n" + itog + "@enduml\n", path_uml)
        showing_pic("vremen1.png")
    else:
        print("такого пакета не нашлось")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Аргументы указаны неверно")
        exit()
    path_uml = sys.argv[1]
    package_name = sys.argv[2]
    main(package_name, path_uml)