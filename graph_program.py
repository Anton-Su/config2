import sys
import os
import subprocess
from PIL import Image
import requests
import gzip
import io

dependencies = {}
output_name = "vremen"


def showing_pic(name):
    path_picture = os.getcwd() + "\\" + name
    if not os.path.exists(path_picture):
        print("picture not found")
        return False
    im = Image.open(path_picture)
    im.show()
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
            itog += f'"{package}" --> "{dep}"\n'
    return itog


def detect_dependencies_recur(file_path, name_package):
    flag = False
    with open(file_path, "r", encoding="utf8") as f:
        for line in f:
            stroka = line.strip()
            if stroka.startswith("Package:") and stroka.split("Package: ")[1] == name_package:
                 dependencies[name_package] = []
                 flag = True
            elif flag and stroka.startswith("Package:"):
                break
            elif flag and stroka.startswith("Depends:"):
                stroka = stroka.replace(" |", ',').split("Depends: ")[1]
                stroka = [i if i.find("(") == -1 else i.split(" (")[0] for i in stroka.split(', ')]
                dependencies[name_package].extend(stroka)
    if flag:
        for i in dependencies[name_package]:
            if i not in dependencies:
                detect_dependencies_recur(file_path, i)
    return dependencies


def get_dependencies(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as gz_file:
                text_content = gz_file.read().decode("utf-8")
                with open(f"{output_name}.txt", "w", encoding="utf-8") as file:
                    file.write(text_content)
                return text_content
        else:
            print(f"Ошибка при загрузке архива: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Ошибка при загрузке: {e}")
    return 1


def main(package_name, path_uml):
    if not os.path.exists(path_uml):
        print('os error')
        return
    get_dependencies("http://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.gz")
    detect_dependencies_recur(f"{output_name}.txt", package_name)
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