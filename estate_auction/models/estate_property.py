from odoo import api, fields, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    property_sale_format = fields.Selection(
        string="Sell Type",
        selection=[
            ('auction', "Auction"),
            ('regular', "Regular"),
        ],
        default='regular'
    )
    auction_stage = fields.Selection(
        string="Auction Stage",
        selection=[
            ('01_template', "Template"),
            ('02_auction', "Auction"),
            ('03_sold', "Sold"),
        ],
        default='01_template',
    )
    auction_end_time = fields.Datetime(string="Auction End Time")
    highest_bidder = fields.Many2one(string="Highest Bidder", comodel_name="res.partner")
    invoice_ids = fields.One2many(string="Invoice", comodel_name="account.move", inverse_name="estate_property_id")
    invoice_count = fields.Integer(string="Invoice Count", compute="_compute_invoice_count")

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = len(record.invoice_ids)

    def _action_close_expired_auctions(self):
        """ Close expired auctions """
        expired_properties = self.search([
            ('property_sale_format', '=', 'auction'),
            ('auction_stage', '=', 'auction'),
            ('auction_end_time', '<', fields.Datetime.now())
        ])
        expired_properties.write([
            ('auction_stage', '=', 'sold')
        ])
        for property in expired_properties:
            if property.offer_ids:
                property.offer_ids.sort(key=lambda offer: offer.price, reverse=True)
                property.offer_ids[0].action_confirm()
                property.write({
                    'state': 'sold',
                    'selling_price': property.offer_ids[0].price,
                    'buyer_id': property.offer_ids[0].partner_id.id
                })
            else:
                property.write({
                    'state': 'cancelled'
                })

    def action_start_auction(self):
        self.auction_stage = '02_auction'
