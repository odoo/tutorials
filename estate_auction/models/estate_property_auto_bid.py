from odoo import fields, models, api

from odoo.exceptions import UserError


class EstatePropertyAutoBid(models.Model):
    _name = "estate.property.auto.bid"
    _description = "Estate Property Auto Bid"
    _order = "id desc"

    property_id = fields.Many2one("estate.property", required=True)
    available_partner_ids = fields.Many2many("res.partner", compute="_compute_available_partner_ids")
    partner_id = fields.Many2one("res.partner", required=True, domain="[('id', 'in', available_partner_ids)]")
    current_bid_price = fields.Float(compute="_compute_current_bid_price")
    increment_amount = fields.Float(string="Increment Amount", required=True, default=1000)
    max_bid_price = fields.Float(required=True)
    state = fields.Selection([
        ('running', 'Running'),
        ('stopped', 'Stopped'),
    ],
    default='running')
    active = fields.Boolean(default=True)

    @api.onchange('max_bid_price')
    def _onchange_max_bid(self):
        for record in self:
            if record.max_bid_price < record.current_bid_price:
                record.state = 'stopped'

    @api.constrains('max_bid_price')
    def _check_max_bid(self):
        for record in self:
            if (record.max_bid_price <= record.current_bid_price):
                raise UserError("Max bid must be greater than current bid.")

    @api.constrains('increment_amount')
    def _check_increment_amount(self):
        for record in self:
            if record.increment_amount < 100:
                raise UserError("Increment amount should be greater than the 100.")

    @api.depends('property_id.offer_ids.price', 'property_id.offer_ids.partner_id')
    def _compute_current_bid_price(self):
        for record in self:
            highest_price = 0
            for offer in record.property_id.offer_ids:
                if (offer.partner_id == record.partner_id):
                    if offer.price > highest_price:
                        highest_price = offer.price
            record.current_bid_price = highest_price

    @api.depends('property_id.offer_ids.partner_id')
    def _compute_available_partner_ids(self):
        for record in self:
            record.available_partner_ids = (record.property_id.offer_ids.mapped('partner_id'))

    @api.model
    def _cron_process_auto_bids(self):
        properties = self.env['estate.property'].search([
            ('state', '=', 'offer_received'),
            ('auction_state', '=', 'in_progress'),
            ('selling_mode', '=', 'auction'),
        ])
        for property_record in properties:
            highest_bidder = property_record.highest_bidder_id
            highest_price = property_record.best_price
            if not highest_bidder:
                continue
            auto_bids = (property_record.auto_bid_ids.filtered(lambda bid: bid.state == 'running'))
            for auto_bid in auto_bids:
                if auto_bid.max_bid_price < auto_bid.current_bid_price:
                    auto_bid.state = 'stopped'
                    continue
                if (auto_bid.partner_id == highest_bidder):
                    continue
                next_bid = (highest_price + auto_bid.increment_amount)
                if (next_bid > auto_bid.max_bid_price):
                    auto_bid.state = 'stopped'
                    continue
                self.env['estate.property.offer'].create({
                    'property_id': property_record.id,
                    'partner_id': auto_bid.partner_id.id,
                    'price': next_bid,
                })
                break
