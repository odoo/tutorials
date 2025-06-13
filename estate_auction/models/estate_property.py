from datetime import datetime

from odoo import api, Command, fields, models
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = 'estate.property'


    selling_type = fields.Selection(
        selection = [
            ('auction', "Auction"),
            ('regular', "Regular")
        ],
        default='regular'
    )

    auction_state = fields.Selection([
        ('template', "Template"),
        ('auction', "Auction"),
        ('done', "Done")
    ],
    string="Auction State",
    default='template',
    required=True
    )

    auction_end_date = fields.Datetime("End Date")
    auction_highest_offer = fields.Integer("Highest Offer", compute="_compute_highest_offer")
    auction_highest_bidder = fields.Many2one('res.partner', "Highest Bidder", compute="_compute_highest_offer")

    @api.depends('offer_ids')
    def _compute_highest_offer(self):
        for record in self:
            if record.offer_ids:
                highest_offer = max(record.offer_ids, key=lambda offer:offer.price)
                record.auction_highest_offer = highest_offer.price
                record.auction_highest_bidder = highest_offer.partner_id
            else:
                record.auction_highest_offer = 0
                record.auction_highest_bidder = None

    def _check_auction_status(self):
        properties = self.search([('selling_type', '=', 'auction'), ('auction_state', '=', 'auction'), ('state', 'in', ['new', 'offer_received'])])
        for property in properties:
            if(datetime.now() > property.auction_end_date):
                property.auction_state = 'done'
                if property.offer_ids:
                    highest_offer = next(filter(lambda offer: offer.price == property.auction_highest_offer, property.offer_ids), None)
                    template = self.env.ref('estate_auction.auction_result_email_template')
                    property.write({
                        'buyer_id' : highest_offer.partner_id,
                        'selling_price' : highest_offer.price,
                        'state' : 'offer_accepted'
                    })

                    for offer in property.offer_ids:
                        offer.status = 'refused' if offer != highest_offer else 'accepted'
                        template.send_mail(offer.id, force_send=True)

    def start_auction(self):
        for record in self:
            if not record.auction_end_date:
                raise UserError("Please Enter Auction End Date First")
            record.auction_state = 'auction'

    def action_sold(self):
        invoice = super().action_sold()
        invoice.property_id = self.id
        return invoice

    def action_view_invoice(self):
        self.ensure_one()
        invoice = self.env['account.move'].search(
            [('property_id', '=', self.id)],
        )
        return {
            'type': 'ir.actions.act_window',
            'name': 'Property Invoice',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('id', '=', invoice.id)],
        }
