from odoo import fields
from odoo.tests import Form

from .common import EstateAuctionCommon


class TestEstateAuctionForm(EstateAuctionCommon):
    _property_form_view = "estate_auction.estate_property_view_form_auction"

    def test_form_defaults_to_regular_sale(self):
        form = Form(self.env["estate.property"], view=self._property_form_view)

        self.assertEqual(form.sale_type, "regular")

    def test_form_auction_requires_end_time_on_save(self):
        form = Form(self.env["estate.property"], view=self._property_form_view)
        form.name = "Test Auction Form Property"
        form.expected_price = 100.0
        form.sale_type = "auction"

        with self.assertRaisesRegex(AssertionError, "auction_end_time is a required field"):
            form.save()

    def test_form_can_create_auction_property_with_end_time(self):
        form = Form(self.env["estate.property"], view=self._property_form_view)
        form.name = "Test Auction Form Property"
        form.expected_price = 100.0
        form.sale_type = "auction"
        expected_end_time = fields.Datetime.to_datetime("2026-04-01 11:00:00")
        form.auction_end_time = fields.Datetime.to_string(expected_end_time)

        property_record = form.save()

        self.assertEqual(property_record.sale_type, "auction")
        self.assertEqual(property_record.auction_end_time, expected_end_time)

    def test_form_sale_type_is_readonly_after_auction_starts(self):
        property_record = self._create_property()
        property_record.action_start_auction()

        form = Form(property_record, view=self._property_form_view)

        with self.assertRaisesRegex(AssertionError, "readonly"):
            form.sale_type = "regular"
