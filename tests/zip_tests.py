from unittest import TestCase, main
import zip_program

config = zip_program.configparser.ConfigParser()
config.read(r'C:\Users\Antua\PycharmProjects\config1\configuration.ini')
name = config.get('User', 'user_name')
archivePath = config.get('ArchivePath', 'path_value')
startScriptPath = config.get('StartScriptPath', 'path_value')


class Random(TestCase):
    def test_cd_1(self):  # "не попал"
        self.assertEqual(zip_program.cd("123", '', archivePath), '')

    def test_cd_2(self):  # путь относительный
        self.assertEqual(zip_program.cd("./1/..//////", 'folder_1/', archivePath), 'folder_1/')

    def test_cd_3(self):  # путь абсолютный
        self.assertEqual(zip_program.cd("/folder_1/./1///////", 'folder_1/', archivePath), 'folder_1/1/')

    def test_ls_1(self):
        self.assertEqual(zip_program.ls(archivePath, ''), ['empty_folder', 'folder_2', 'originally_folder', 'hm.txt', 'privet.txt', 'wc_1.txt', 'wc_2.txt', 'folder_1'])

    def test_ls_2(self):
        self.assertEqual(zip_program.ls(archivePath, 'folder_1/1/hey-hey/'), ['normal_photo_1.jpg', 'normal_photo_2.jpg', 'test.txt', 'testirovanie.txt'])

    def test_ls_3(self):  # пусто
        self.assertEqual(zip_program.ls(archivePath, 'empty_folder/'), [])

    def test_wc_1(self):  # картинка
        self.assertEqual(zip_program.wc('/folder_1/./1///./././/hey-hey/normal_photo_1.jpg', 'folder/', archivePath), f"\t {90} \t {544} \t {24826}")

    def test_wc_2(self):  # файл
        self.assertEqual(zip_program.wc('info.txt', 'folder_1/2/', archivePath), f"\t {1} \t {4} \t {22}")

    def test_wc_3(self):  # не найдено
        self.assertEqual(zip_program.wc('info1.txt', 'folder_1/2/', archivePath), None)
