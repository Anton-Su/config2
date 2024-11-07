import sys
import os

path_to_name_package = os.getcwd() + "\\dependencies.txt"
dependencies = {}


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
                #detect_dependencies_recur(file_path, stroka.split(": ")[1])
    if flag:
        for i in dependencies[name_package]:
            if i not in dependencies:
                detect_dependencies_recur(file_path, i)
        # for line in f:
        #     line = line.strip()
        #     if line == name_package:
        #
        #         pass
        #     if line:
        #         if not line.startswith("Depends:"):
        #             current_package = line
        #             dependencies[current_package] = []
        #         else:
        #             dep_package = line.split(": ")[1]
        #             dependencies[current_package].append(dep_package)
    print(dependencies)


def main(path_uml, package_name):
    if not os.path.exists(path_uml) or not os.path.exists(path_to_name_package):
        print('os error')
        return
    detect_dependencies_recur(path_to_name_package, package_name)
    # if path_uml
    # print(path_uml)
    print(1)
    pass


if __name__ == "__main__":
    path_to_uml = "D:\downloads\plantuml-1.2024.7.jar"
    package_name = "libcurl4"
    if len(sys.argv) == 1: # 3
        #path_uml = sys.argv[1]
        #package_name = sys.argv[2]
        main(path_to_name_package, package_name)