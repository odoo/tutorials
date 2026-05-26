from odoo import models, fields, api

from odoo.exceptions import UserError,ValidationError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    selling_mode = fields.Selection([
            ('regular', 'Regular'),
            ('auction', 'Auction')
        ],
        string="Selling Mode", default='regular', required=True)

    auction_state = fields.Selection([
            ('draft', 'Draft'),
            ('in_progress', 'In Progress'),
            ('ended', 'Ended'),
            ('sold', 'Sold')
        ],
        string="Auction State", default='draft', readonly=True)
    auction_end = fields.Datetime(string="Auction End Time")
    # highest_offer = fields.Float(string="Highest Offer", compute="_compute_best_price", readonly=True)
    highest_bidder_id = fields.Many2one("res.partner", string="Highest Bidder", compute="_compute_best_price", readonly=True)

    @api.onchange('selling_mode')
    def _onchange_selling_mode(self):
        for record in self:
            if record.selling_mode == 'auction':
                record.auction_state = 'draft'
            else:
                record.auction_state = False

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        super()._compute_best_price()
        for record in self:
            highest_offer = record.offer_ids[:1]
            record.highest_bidder_id = highest_offer.partner_id

    def write(self, vals):
        for record in self:
            if (vals.get('selling_mode') == 'regular' and record.auction_state in ['in_progress', 'sold', 'ended']):
                raise ValidationError("You cannot change selling mode after auction starts.")
        return super().write(vals)

    @api.model
    def _cron_close_auction(self, job_count=20):
        domain = [
            ('selling_mode', '=', 'auction'),
            ('auction_state', '=', 'in_progress'),
            ('auction_end', '<=', fields.Datetime.now())
        ]
        expired_auction_offer = self.search(domain, order= 'auction_end asc', limit=job_count)

        accepted_template = self.env.ref('estate_auction.email_template_auction_offer_accepted')
        rejected_template = self.env.ref('estate_auction.email_template_auction_offer_rejected')

        for property_record in expired_auction_offer:
            high_offer =property_record.offer_ids[:1]
            if high_offer:
                high_offer.action_accept()
                high_offer.property_id._mark_as_sold()
                property_record.auction_state = 'sold'

                accepted_template.send_mail(high_offer.id, force_send=True)
                rejected_offers = property_record.offer_ids.filtered(lambda offer: offer.id != high_offer.id)
                for offer in rejected_offers:
                    rejected_template.send_mail(offer.id, force_send=True)
            else:
                property_record.auction_state = 'ended'

    def action_start_auction(self):
        for record in self:
            if record.selling_mode != 'auction':
                raise UserError("This property is not auction type.")
            if not record.auction_end:
                raise UserError("Please set auction end time.")
            record.auction_state = 'in_progress'

    def action_end_auction(self):
        for record in self:
            # if not record.offer_ids:
            #     raise UserError("Atleast add one offer")
            high_offer = record.offer_ids[:1]
            if high_offer:
                high_offer.action_accept()
                record.auction_state = 'sold'
            else:
                record.auction_state = 'ended'

