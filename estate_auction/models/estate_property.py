from datetime import timedelta
from odoo import api, fields, models

STATUS_COLOR = {
    'on_track': 20,        # green / success --- template
    'at_risk': 22,         # orange -----auction
    'off_track': 23,       # red / danger -----sold
    False: 0,              # default grey -- for studio
    'to_define': 0,        # Only used in project.task
}


class EstateProperty(models.Model):

    _inherit = 'estate.property'

    auction_end_time = fields.Datetime(
        string="Auction End Date",
        compute="_compute_auction_end_time",
        store=True,
        copy=False
    )

    is_auction_started = fields.Boolean(
        compute="_compute_is_auction_started",
        default=False
    )

    bid_type = fields.Selection(
        [('auction', 'Auction'), ('regular', 'Regular')],
        string="Bid Type",
        default='auction',
        copy=False,
        tracking=True
    )

    auction_status = fields.Selection(
        [
            ('auction_not_begun', 'Auction Not Started'),
            ('auction_started', 'Auction Started'),
            ('auction_ended', 'Auction Ended')
        ],
        string="Auction Status",
        default='auction_not_begun',
        copy=False,
        tracking=True
    )

    auction_update_status = fields.Selection(
        selection=[
            ('on_track', 'Template'),
            ('at_risk', 'Audition'),
            ('off_track', 'Sold'),
            ('to_define', 'To Define')
        ],
        default='to_define',
        store=True,
        readonly=False,
        required=True
    )

    auction_stage_color = fields.Integer(
        compute="_compute_auction_stage_color",
        store=True
    )

    invoice_count = fields.Integer(
        string="Invoices",
        compute="_compute_invoice_count"
    )

    highest_offer = fields.Float(
        string="Highest Offer",
        compute="_compute_highest_offer",
        readonly=True
    )

    highest_bidder = fields.Many2one(
        "res.partner",
        string="Highest Bidder",
        readonly=True
    )

    def start_auction(self):
        if not self.is_auction_started and not self.auction_end_time:
            self.write({
                'auction_end_time': fields.Datetime.now() + timedelta(days=10),
                'is_auction_started': True,
                'highest_offer': 0.0,
                'highest_bidder': False,
                'auction_status': 'auction_started',
                'auction_update_status': 'at_risk'
            })

    @api.depends('auction_update_status')
    def _compute_auction_stage_color(self):
        for record in self:
            record.auction_stage_color = STATUS_COLOR[record.auction_update_status]

    @api.depends("offer_ids.price")
    def _compute_highest_offer(self):
        for record in self:
            record.highest_offer = max(record.mapped('offer_ids.price'), default=0)
            highest_bid_offer_id = record.offer_ids.filtered(lambda o: o.price == record.highest_offer)
            record.highest_bidder = highest_bid_offer_id.partner_id

    @api.depends("auction_end_time", "auction_status")
    def _compute_is_auction_started(self):
        for record in self:
            if record.auction_end_time and record.auction_end_time < fields.Datetime.now():
                highest_bid = max(record.mapped('offer_ids.price'), default=0)
                highest_bid_offer = record.offer_ids.filtered(lambda o: o.price == highest_bid)[:1]

                record.write({
                    'is_auction_started': False,
                    'auction_status': 'auction_ended',
                    'selling_price': highest_bid,
                    'buyer_id': highest_bid_offer.partner_id.id if highest_bid_offer else False
                })
            elif record.auction_status == "auction_started":
                record.is_auction_started = True
            else:
                record.is_auction_started = False

    def check_and_end_auction(self):
        for record in self.search([('auction_status', '=', 'auction_started')]):
            if record.auction_end_time and record.auction_end_time < fields.Datetime.now():
                record.auction_status = 'auction_ended'
                record.is_auction_started = False
                highest_bid = max(record.mapped('offer_ids.price'), default=0)
                highest_bid_offer = record.offer_ids.filtered(lambda o: o.price == highest_bid)[:1]

                record.write({
                    'auction_status': 'auction_ended',
                    'is_auction_started': False,
                    'selling_price': highest_bid,
                    'buyer_id': highest_bid_offer.partner_id.id if highest_bid_offer else False
                })

    @api.depends("bid_type")
    def _compute_auction_end_time(self):
        for record in self:
            if record.bid_type != "auction":
                record.auction_end_time = False
                record.is_auction_started = False
                record.auction_status = "auction_not_begun"
                record.auction_update_status = "on_track"

    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = self.env["account.move"].search_count([
                ("partner_id", "=", record.buyer_id.id),
                ("move_type", "=", "out_invoice"),
                ("state", "!=", "cancel"),
            ])

    def create_invoice(self):
        for record in self:
            if not record.buyer_id:
                raise ValueError("A buyer must be assigned before creating an invoice.")

            self.env["account.move"].create({
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    (0, 0, {
                        "name": record.name,
                        "quantity": 1,
                        "price_unit": record.selling_price
                    })
                ],
            })

    def action_view_invoice(self):
        self.ensure_one()
        invoices = self.env["account.move"].search([
            ("partner_id", "=", self.buyer_id.id),
            ("move_type", "=", "out_invoice"),
            ("state", "!=", "cancel")
        ])

        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "domain": [("id", "in", invoices.ids)],
            "context": {"create": False, "default_move_type": "out_invoice"},
            "name": "Customer Invoices",
            "view_mode": "list,form",
        }
