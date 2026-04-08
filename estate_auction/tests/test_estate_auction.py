from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import freeze_time

from .common import EstateAuctionCommon


class TestEstateAuction(EstateAuctionCommon):

    def test_auction_property_requires_end_time(self):
        with self.assertRaises(ValidationError):
            self._create_property(auction_end_time=False)

    def test_action_start_auction_sets_state(self):
        property_record = self._create_property()

        property_record.action_start_auction()

        self.assertEqual(property_record.state, "auction")

    def test_action_start_auction_rejects_regular_sale(self):
        property_record = self._create_property(sale_type="regular")

        with self.assertRaisesRegex(ValidationError, "Only properties in Auction mode can start an auction."):
            property_record.action_start_auction()

    def test_action_start_auction_rejects_past_end_time(self):
        property_record = self._create_property(
            auction_end_time=fields.Datetime.to_string(
                fields.Datetime.now() - timedelta(hours=1),
            ),
        )

        with self.assertRaisesRegex(ValidationError, "Auction end time must be in the future."):
            property_record.action_start_auction()

    def test_action_start_auction_rejects_sold_property(self):
        property_record = self._create_property(state="sold")

        with self.assertRaisesRegex(
            ValidationError,
            "You cannot start an auction for sold, canceled, or accepted properties.",
        ):
            property_record.action_start_auction()

    def test_action_start_auction_rejects_canceled_property(self):
        property_record = self._create_property(state="canceled")

        with self.assertRaisesRegex(
            ValidationError,
            "You cannot start an auction for sold, canceled, or accepted properties.",
        ):
            property_record.action_start_auction()

    def test_action_start_auction_rejects_offer_accepted_property(self):
        property_record = self._create_property(state="offer_accepted")

        with self.assertRaisesRegex(
            ValidationError,
            "You cannot start an auction for sold, canceled, or accepted properties.",
        ):
            property_record.action_start_auction()

    def test_action_start_auction_rejects_already_running_auction(self):
        property_record = self._create_property()
        property_record.action_start_auction()

        with self.assertRaisesRegex(ValidationError, "Auction is already running for this property."):
            property_record.action_start_auction()

    def test_regular_offer_keeps_base_behavior_and_never_sets_auction_flag(self):
        property_record = self._create_property(sale_type="regular")

        offer = self._create_offer(property_record, self.partner_a, 120.0)
        property_record = self.env["estate.property"].browse(property_record.id)

        self.assertFalse(offer.is_auction_bid)
        self.assertEqual(property_record.state, "offer_received")

    def test_auction_bid_requires_running_auction(self):
        property_record = self._create_property()

        with self.assertRaisesRegex(ValidationError, "Cannot add bids unless the auction is active."):
            self._create_offer(property_record, self.partner_a, 120.0)

        property_record = self.env["estate.property"].browse(property_record.id)
        self.assertFalse(property_record.offer_ids)
        self.assertEqual(property_record.state, "new")

    def test_lower_auction_bid_than_current_best_is_rejected(self):
        property_record = self._create_property()
        property_record.action_start_auction()
        self._create_offer(property_record, self.partner_a, 150.0)

        with self.assertRaisesRegex(UserError, "An offer with higher price already exists"):
            self._create_offer(property_record, self.partner_b, 120.0)

    @freeze_time("2026-04-01 10:00:00")
    def test_expired_auction_rejects_new_bid(self):
        property_record = self._create_property()
        property_record.action_start_auction()

        with freeze_time("2026-04-02 12:00:00"):
            with self.assertRaisesRegex(ValidationError, "Cannot add bids to an auction that has already ended."):
                self._create_offer(property_record, self.partner_a, 120.0)

    def test_auction_bid_is_flagged_and_property_stays_in_auction(self):
        property_record = self._create_property()
        property_record.action_start_auction()

        offer = self._create_offer(property_record, self.partner_a, 120.0)
        property_record = self.env["estate.property"].browse(property_record.id)

        self.assertTrue(offer.is_auction_bid)
        self.assertEqual(property_record.state, "auction")

    def test_running_auction_blocks_manual_accept_and_refuse(self):
        property_record = self._create_property()
        property_record.action_start_auction()
        offer = self._create_offer(property_record, self.partner_a, 120.0)

        with self.assertRaises(ValidationError):
            offer.action_accept()
        with self.assertRaises(ValidationError):
            offer.action_refuse()

    @freeze_time("2026-04-01 10:00:00")
    def test_accepting_expired_auction_bid_refuses_remaining_bids(self):
        property_record = self._create_property()
        property_record.action_start_auction()
        low_offer = self._create_offer(property_record, self.partner_a, 120.0)
        high_offer = self._create_offer(property_record, self.partner_b, 150.0)

        with freeze_time("2026-04-02 12:00:00"):
            high_offer.action_accept()

        property_record = self.env["estate.property"].browse(property_record.id)
        low_offer = self.env["estate.property.offer"].browse(low_offer.id)
        high_offer = self.env["estate.property.offer"].browse(high_offer.id)
        self.assertEqual(high_offer.status, "accepted")
        self.assertEqual(low_offer.status, "refused")
        self.assertEqual(property_record.buyer_id, self.partner_b)
        self.assertEqual(property_record.selling_price, 150.0)

    def test_action_view_invoice_returns_false_when_missing(self):
        property_record = self._create_property()

        self.assertFalse(property_record.action_view_invoice())

    @freeze_time("2026-04-01 10:00:00")
    def test_expired_auction_without_valid_bids_moves_to_template(self):
        property_record = self._create_property()
        property_record.action_start_auction()

        with freeze_time("2026-04-02 12:00:00"):
            self.env["estate.property"]._cron_process_expired_auctions()

        property_record = self.env["estate.property"].browse(property_record.id)
        self.assertEqual(property_record.state, "template")

    def test_cron_does_nothing_when_no_auction_is_expired(self):
        property_record = self._create_property()
        property_record.action_start_auction()
        offer = self._create_offer(property_record, self.partner_a, 120.0)

        self.env["estate.property"]._cron_process_expired_auctions()

        property_record = self.env["estate.property"].browse(property_record.id)
        offer = self.env["estate.property.offer"].browse(offer.id)
        self.assertEqual(property_record.state, "auction")
        self.assertFalse(offer.status)
        self.assertFalse(property_record.invoice_ids)
