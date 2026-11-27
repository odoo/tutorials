from odoo.tests.common import TransactionCase


class BasicPythonStuffCase(TransactionCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_upper2(self):
        self.assertTrue('FOO'.isupper())

    def test_split(self):
        s = 'hello world'
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
