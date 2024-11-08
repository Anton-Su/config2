from unittest import TestCase
import graph_program

path_to_uml = r"C:\Users\Antua\PycharmProjects\config2\plantuml-1.2024.7.jar"


class Random(TestCase):
    def test_detect_1(self):  # "зависимость 1"
        example = "test1.txt"
        self.assertEqual(graph_program.detect_dependencies_recur(example, "curl"),
                         {'curl': ['libc6', 'libcurl4', 'zlib1g'], 'libc6': ['libgcc-s1', 'libcrypt1', 'libidn2-0'],
                          'libcurl4': ['libc6', 'libgnutls30', 'libssh-4', 'zlib1g'], 'zlib1g': ['libc6']})

    def test_detect_2(self):  # "зависимость 2"
        example = "test2.txt"
        graph_program.dependencies = {}
        self.assertEqual(graph_program.detect_dependencies_recur(example, "openssl"),
                         {'openssl': ['libc6', 'libssl3', 'zlib1g'], 'libssl3': ['libc6', 'libcrypto3'],
                          'libcrypto3': ['libc6'], 'libc6': ['libgcc-s1', 'libpthread'], 'zlib1g': ['libc6']})

    def test_detect_3(self):  # "зависимость 3"
        example = "test3.txt"
        graph_program.dependencies = {}
        self.assertEqual(graph_program.detect_dependencies_recur(example, "libxml2"),
                         {'libxml2': ['zlib1g', 'libicu66', 'liblzma5'], 'libicu66': ['libc6', 'libgcc-s1'],
                          'liblzma5': ['libc6'], 'libc6': ['libgcc-s1', 'libpthread'], 'zlib1g': ['libc6']})

    def test_transform_1(self):
        graph_program.dependencies = {'curl': ['libc6', 'libcurl4', 'zlib1g'],
                                      'libc6': ['libgcc-s1', 'libcrypt1', 'libidn2-0'],
                                      'libcurl4': ['libc6', 'libgnutls30', 'libssh-4', 'zlib1g'],
                                      'zlib1g': ['libc6']}
        self.assertEqual(graph_program.transform_to_uml_format(), '"curl" --> "libc6"\n"curl" --> "libcurl4"\n"curl" --> '
                                                                  '"zlib1g"\n"libc6" --> "libgcc-s1"\n"libc6" --> '
                                                                  '"libcrypt1"\n"libc6" --> "libidn2-0"\n"libcurl4" --> '
                                                                  '"libc6"\n"libcurl4" --> "libgnutls30"\n"libcurl4" --> '
                                                                  '"libssh-4"\n"libcurl4" --> "zlib1g"\n"zlib1g" --> "libc6"\n')

    def test_transform_2(self):
        graph_program.dependencies = {'openssl': ['libc6', 'libssl3', 'zlib1g'], 'libssl3': ['libc6', 'libcrypto3'],
                                      'libcrypto3': ['libc6'], 'libc6': ['libgcc-s1', 'libpthread'],
                                      'zlib1g': ['libc6']}
        self.assertEqual(graph_program.transform_to_uml_format(), '"openssl" --> "libc6"\n"openssl" --> "libssl3"\n"openssl" '
                                                                  '--> "zlib1g"\n"libssl3" --> "libc6"\n"libssl3" --> '
                                                                  '"libcrypto3"\n"libcrypto3" --> "libc6"\n"libc6" --> '
                                                                  '"libgcc-s1"\n"libc6" --> "libpthread"\n"zlib1g" --> "libc6"\n')

    def test_transform_3(self):
        graph_program.dependencies = {'libxml2': ['zlib1g', 'libicu66', 'liblzma5'], 'libicu66': ['libc6', 'libgcc-s1'],
                                      'liblzma5': ['libc6'], 'libc6': ['libgcc-s1', 'libpthread'], 'zlib1g': ['libc6']}
        self.assertEqual(graph_program.transform_to_uml_format(), '"libxml2" --> "zlib1g"\n"libxml2" --> "libicu66"\n"libxml2" '
                                                                  '--> "liblzma5"\n"libicu66" --> "libc6"\n"libicu66" --> '
                                                                  '"libgcc-s1"\n"liblzma5" --> "libc6"\n"libc6" --> '
                                                                  '"libgcc-s1"\n"libc6" --> "libpthread"\n"zlib1g" --> "libc6"\n')

    def test_showing1(self):  # нашлась
        self.assertEqual(graph_program.showing_pic("vremen.png"), True)

    def test_showing2(self):  # не нашлось
        self.assertEqual(graph_program.showing_pic("vremen12.png"), False)

    def test_render(self):  # нашлась
        uml_text = '@startuml\nlibxml2 --> zlib1g\nlibxml2 --> libicu66\nlibxml2 --> liblzma5\nlibicu66 --> ' \
                   'libc6\nlibicu66 --> libgcc-s1\nliblzma5 --> libc6\nlibc6 --> libgcc-s1\nlibc6 --> ' \
                   'libpthread\nzlib1g --> libc6\n@enduml\n'
        self.assertEqual(graph_program.render_plantuml_file(uml_text, path_to_uml), True)
