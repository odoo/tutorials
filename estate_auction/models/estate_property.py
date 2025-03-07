from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import datetime

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    selling_type = fields.Selection([
        ('regular', 'Regular'),
        ('auction', 'Auction'),
    ], string='Auction Type', default='regular')

    auction_state = fields.Selection([
        ('template', 'Template'),
        ('auction', 'Auction'),
        ('done', 'Done')
    ],
    string = 'Auction State',
    default='template',
    required=True
    )

    auction_end_time = fields.Datetime(string='Auction End Time')
    highest_offer = fields.Float(string='Highest Offer', readonly=True, compute='_compute_auction_details', store=True)
    highest_bidder_id = fields.Many2one('res.partner', string='Highest Bidder', readonly=True, compute='_compute_auction_details', store=True)

    @api.depends('offer_ids', 'selling_type')
    def _compute_auction_details(self):
        for record in self:
            if record.selling_type == 'auction' and record.offer_ids:
                highest_offer = 0.0
                highest_bidder = False
                for offer in record.offer_ids:
                    if offer.price > highest_offer:
                        highest_offer = offer.price
                        highest_bidder = offer.partner_id.id
                record.highest_offer = highest_offer
                record.highest_bidder_id = highest_bidder
            else:
                record.highest_offer = 0.0
                record.highest_bidder_id = False

    def action_start_auction(self):
        for record in self:
            if not record.auction_end_time:
                raise UserError("Please Enter Auction End Date First")
            record.auction_state = 'auction'
        
    def _check_auction_status(self):
        current_time = fields.Datetime.now()
        properties = self.search([
            ('selling_type', '=', 'auction'),
            ('auction_end_time', '<=', current_time),
            ('state', '=', 'offer_recieved')
        ])

        for property in properties:
            highest_offer = property.offer_ids.sorted(key=lambda o: o.price, reverse=True)

            if highest_offer:
                highest_offer = highest_offer[0]
                highest_offer.write({'status': 'accepted'})

                for offer in property.offer_ids:
                    if offer != highest_offer:
                        offer.write({'status': 'refused'})

                property.write({
                    'selling_price': highest_offer.price,
                    'buyer_id': highest_offer.partner_id.id,
                    'state': 'offer_accepted'
                })

                template = self.env.ref('estate_auction.email_template_offer_accepted')
                template.sudo().send_mail(highest_offer.partner_id.id, force_send=True)

                rejected_offers = property.offer_ids.filtered(lambda o: o != highest_offer)
                template_rejected = self.env.ref('estate_auction.email_template_offer_rejected')

                for offer in rejected_offers:
                    template_rejected.sudo().send_mail(offer.partner_id.id, force_send=True)
            else:
                property.write({'state': 'cancelled'})
