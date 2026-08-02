import unittest


class StartupTest(unittest.TestCase):
    def test_import_main_does_not_raise(self):
        import main

        self.assertTrue(hasattr(main, "app"))


if __name__ == "__main__":
    unittest.main()
