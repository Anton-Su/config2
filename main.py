import sys
import os
import subprocess

path_to_name_package = os.getcwd() + "\\dependencies.txt"
dependencies = {}


def showing_pic(name):
    if os.name == "nt": # winda
        subprocess.run(["start", os.getcwd() + "\\" + name], shell=True)
    else:
        subprocess.run(["xdg-open", os.getcwd() + "\\" + name])


def render_plantuml_file(uml_text, path_to_uml):
    with open("vremen.puml", "w") as f:
        f.write(uml_text)
    try:
        subprocess.run(["java", "-jar", path_to_uml, "vremen.puml"], check=True)
    except subprocess.CalledProcessError as e:
        print("Ошибка при запуске PlantUML:", e)


def transform_to_uml_format():
    itog = ''
    for package, deps in dependencies.items():
        for dep in deps:
            itog += f"{package} --> {dep}\n"
    itog = "@startuml\n" + itog + "@enduml\n"
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


def main(package_name, path_uml):
    if not os.path.exists(path_uml) or not os.path.exists(path_to_name_package):
        print('os error')
        return
    detect_dependencies_recur(path_to_name_package, package_name)
    itog = transform_to_uml_format()
    render_plantuml_file(itog, path_to_uml)
    showing_pic("vremen.png")


if __name__ == "__main__":
    path_to_uml = r"C:\Users\Antua\PycharmProjects\config2\plantuml-1.2024.7.jar"
    package_name = "libcurl4"
    if len(sys.argv) == 1: # 3
        #path_uml = sys.argv[1]
        #package_name = sys.argv[2]
        main(package_name, path_to_uml)