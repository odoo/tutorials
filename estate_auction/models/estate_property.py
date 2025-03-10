from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import datetime

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    selling_method = fields.Selection(
        selection = [
            ('auction', "Auction"),
            ('regular', "Regular")
        ],
        default='regular'
    )

    auction_state = fields.Selection([
        ('template', 'Template'),
        ('auction', 'Auction'),
        ('done', 'Done')
    ],
    string='Auction State',
    default='template',
    required=True
    )

    auction_end_time = fields.Datetime("End Time")
    highest_offer = fields.Integer("Highest Offer", compute="_compute_offer_details")
    highest_bidder = fields.Many2one('res.partner', "Highest Bidder", compute="_compute_offer_details")

    @api.depends('offer_ids')
    def _compute_offer_details(self):
        for record in self:
            if record.offer_ids:
                highest_offer = max(record.offer_ids, key=lambda offer:offer.price)
                record.highest_offer = highest_offer.price
                record.highest_bidder = highest_offer.partner_id
            else:
                record.highest_offer = 0
                record.highest_bidder = None

    def action_start_auction(self):
        for record in self:
            if not record.auction_end_time:
                raise UserError("Please Enter Auction End Time")
            record.auction_state = 'auction'

    def _check_auction_status(self):

        curr_time = datetime.now()
        properties = self.search([('selling_method', '=', 'auction'), ('auction_state', '=', 'auction'), ('state', 'in', ['new', 'offer_received'])])
        for property in properties:
            if(curr_time > property.auction_end_time):
                property.auction_state = 'done'
                if property.offer_ids:
                    highest_offer = max(property.offer_ids, key=lambda offer:offer.price)
                    email_template_accepted = self.env.ref('estate_auction.email_template_offer_accepted')
                    email_template_rejected = self.env.ref('estate_auction.email_template_offer_rejected')
                    property.write({
                        'buyer_id' : highest_offer.partner_id,
                        'selling_price' : highest_offer.price,
                        'state' : 'offer_accepted'
                    })

                    for offer in property.offer_ids:
                        if offer != highest_offer:
                            offer.status = 'refused'
                            email_template_rejected.send_mail(offer.id, force_send=True)
                        else:
                            offer.status = 'accepted'
                            email_template_accepted.send_mail(offer.id, force_send=True)
