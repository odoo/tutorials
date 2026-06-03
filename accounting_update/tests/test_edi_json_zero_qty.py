from freezegun import freeze_time

from odoo.addons.l10n_in.tests.common import L10nInTestInvoicingCommon
from odoo.tests import tagged
from odoo import fields


@tagged("post_install", "-at_install")
class TestEdiJsonZeroQty(L10nInTestInvoicingCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_a.l10n_in_gst_treatment = "regular"
        cls.invoice_with_zero_qty = cls._create_invoice_one_line(
            product_id=cls.product_a, invoice_date=fields.Date.from_string("2019-01-01")
        )
        cls.invoice_with_zero_qty.write(
            {
                "invoice_line_ids": [
                    (1, l_id, {"is_zero_qty": True})
                    for l_id in cls.invoice_with_zero_qty.invoice_line_ids.ids
                ]
            }
        )
        cls.invoice_with_zero_qty.action_post()
        with freeze_time("2023-12-25"):
            cls.credit_note_with_zero_qty = cls.invoice_with_zero_qty._reverse_moves()
            cls.credit_note_with_zero_qty.action_post()

        cls.invoice_without_zero_qty = cls._create_invoice_one_line(
            product_id=cls.product_a, invoice_date=fields.Date.from_string("2019-01-01")
        )
        cls.invoice_without_zero_qty.action_post()
        with freeze_time("2023-12-25"):
            cls.credit_note_without_zero_qty = (
                cls.invoice_without_zero_qty._reverse_moves()
            )
            cls.credit_note_without_zero_qty.action_post()

    def test_edi_json(self):
        # line1: 1000 and a tax of 5%
        # 1000 * 1.05 = 1050
        # total tax: 50
        expected = {
            "Version": "1.1",
            "TranDtls": {
                "TaxSch": "GST",
                "SupTyp": "B2B",
                "RegRev": "N",
                "IgstOnIntra": "N",
            },
            "DocDtls": {"Typ": "INV", "No": "INV/18-19/0001", "Dt": "01/01/2019"},
            "SellerDtls": {
                "Addr1": "Khodiyar Chowk",
                "Loc": "Amreli",
                "Pin": 365220,
                "Stcd": "24",
                "Addr2": "Sala Number 3",
                "LglNm": "Default Company",
                "GSTIN": "24AAGCC7144L6ZE",
            },
            "BuyerDtls": {
                "Addr1": "Karansinhji Rd",
                "Loc": "Rajkot",
                "Pin": 360001,
                "Stcd": "24",
                "Addr2": "Karanpara",
                "POS": "24",
                "LglNm": "Partner Intra State",
                "GSTIN": "24ABCPM8965E1ZE",
            },
            "ItemList": [
                {
                    "SlNo": "1",
                    "PrdDesc": "product_a",
                    "IsServc": "N",
                    "HsnCd": "111111",
                    "Qty": 0.0,
                    "Unit": "UNT",
                    "UnitPrice": 1000.0,
                    "TotAmt": 1000.0,
                    "Discount": 0.0,
                    "AssAmt": 1000.0,
                    "GstRt": 5.0,
                    "IgstAmt": 0.0,
                    "CgstAmt": 25.0,
                    "SgstAmt": 25.0,
                    "CesRt": 0.0,
                    "CesAmt": 0.0,
                    "CesNonAdvlAmt": 0.0,
                    "StateCesRt": 0.0,
                    "StateCesAmt": 0.0,
                    "StateCesNonAdvlAmt": 0.0,
                    "OthChrg": 0.0,
                    "TotItemVal": 1050.0,
                },
            ],
            "ValDtls": {
                "AssVal": 1000.0,
                "CgstVal": 25.0,
                "SgstVal": 25.0,
                "IgstVal": 0.0,
                "CesVal": 0.0,
                "StCesVal": 0.0,
                "Discount": 0.0,
                "RndOffAmt": 0.0,
                "TotInvVal": 1050.0,
            },
        }

        with self.subTest(scenario="Invoice with zero qty"):
            json_value = self.invoice_with_zero_qty._l10n_in_edi_generate_invoice_json()
            self.assertDictEqual(
                json_value,
                expected,
                "Indian EDI with zero qty json value is not matched",
            )

        with self.subTest(scenario="Credit Note with zero qty"):
            expected.update(
                {
                    "DocDtls": {
                        "Typ": "CRN",
                        "No": "RINV/23-24/0001",
                        "Dt": "25/12/2023",
                    }
                }
            )
            self.assertDictEqual(
                self.credit_note_with_zero_qty._l10n_in_edi_generate_invoice_json(),
                expected,
                "Indian E-invoice Credit note with zero qty json value is not matched",
            )

        with self.subTest(scenario="Invoice without zero qty"):
            expected.update(
                {
                    "DocDtls": {
                        "Typ": "INV",
                        "No": "INV/18-19/0002",
                        "Dt": "01/01/2019",
                    },
                    "ItemList": [
                        {
                            "SlNo": "1",
                            "PrdDesc": "product_a",
                            "IsServc": "N",
                            "HsnCd": "111111",
                            "Qty": 1.0,
                            "Unit": "UNT",
                            "UnitPrice": 1000.0,
                            "TotAmt": 1000.0,
                            "Discount": 0.0,
                            "AssAmt": 1000.0,
                            "GstRt": 5.0,
                            "IgstAmt": 0.0,
                            "CgstAmt": 25.0,
                            "SgstAmt": 25.0,
                            "CesRt": 0.0,
                            "CesAmt": 0.0,
                            "CesNonAdvlAmt": 0.0,
                            "StateCesRt": 0.0,
                            "StateCesAmt": 0.0,
                            "StateCesNonAdvlAmt": 0.0,
                            "OthChrg": 0.0,
                            "TotItemVal": 1050.0,
                        },
                    ],
                }
            )
            json_value = (
                self.invoice_without_zero_qty._l10n_in_edi_generate_invoice_json()
            )
            self.assertDictEqual(
                json_value,
                expected,
                "Indian E-invoice without zero qty json value is not matched",
            )

        with self.subTest(scenario="Credit Note without zero qty"):
            expected.update(
                {
                    "DocDtls": {
                        "Typ": "CRN",
                        "No": "RINV/23-24/0002",
                        "Dt": "25/12/2023",
                    }
                }
            )
            self.assertDictEqual(
                self.credit_note_without_zero_qty._l10n_in_edi_generate_invoice_json(),
                expected,
                "Indian E-invoice Credit note without zero qty json value is not matched",
            )
