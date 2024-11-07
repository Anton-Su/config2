from unittest import TestCase, main
import graph_program

# path_to_uml = r"C:\Users\Antua\PycharmProjects\config2\plantuml-1.2024.7.jar"
# package_name = "libcurl4"


class Random(TestCase):
    def test_cd_1(self):  # "не попал"
        self.assertEqual(graph_program.cd("123", '', archivePath), '')

    def test_cd_2(self):  # путь относительный
        self.assertEqual(graph_program.cd("./1/..//////", 'folder_1/', archivePath), 'folder_1/')

    def test_cd_3(self):  # путь абсолютный
        self.assertEqual(graph_program.cd("/folder_1/./1///////", 'folder_1/', archivePath), 'folder_1/1/')
