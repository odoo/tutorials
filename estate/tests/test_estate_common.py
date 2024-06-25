from odoo.tests import TransactionCase


class EstateCommonTest(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner = cls.env["res.partner"].create({"name": "Azure Interior"})
