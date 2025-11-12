from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime

class EstatePropertyModel(models.Model):
    _inherit="estate.property"

    sale_mode = fields.Selection([
        ("auction", "Auction"),
        ("regular", "Regular")
    ])
    auction_end_date = fields.Datetime("End Time")
    auction_highest_offer = fields.Float("Highest Offer", readonly=True)
    auction_highest_bidder= fields.Many2one("res.partner", string="Highest Bidder", readonly=True)
    auction_stage = fields.Selection([
        ("template", "Template"),
        ("auction", "Auction"),
        ("sold", "Sold"),
    ], default="template")
    auction_start= fields.Boolean(default=False)


    def action_start_auction(self):
        if not self.auction_end_date:
            raise ValidationError("Please enter the auction end date and time")
        elif self.auction_end_date<=datetime.now():
            raise ValidationError("Plese enter the valid date and time")
        self.auction_start = True
        self.auction_stage = 'auction'

    def action_end_auction(self):
        self.auction_start = False
    
    def action_set_sold(self):
        super().action_set_sold()
        for record in self:
            if record.state == "sold":  
                record.auction_stage = 'sold'
        return True
    
    @api.depends("auction_stage")
    def _compute_state_from_stage(self):
        for record in self:
            if record.auction_stage == "sold" and record.state != "sold":
                record.state = "sold"
                record.action_set_sold()

    def accept_offer_after_auction_time_end(self):
        properties = self.env['estate.property'].search([
            ('auction_start', '=', True),
            ('auction_end_date', '<=', datetime.now())
        ])
        for record in properties:
                record.auction_start= False
                highest_offer= record.env['estate.property.offer'].search([('property_id', '=', record.id)], order="price desc", limit=1)
                if highest_offer:
                    record.state="offer_accepted"
                    highest_offer.status="accepted"
                    record.selling_price= highest_offer.price
                    record.buyer_id= highest_offer.partner_id
                    accept_template = self.env.ref("auction_real_estate.email_template_offer_accept")
                    if accept_template:
                        accept_template.send_mail(highest_offer.id, force_send=True)

                    for offer in record.offer_ids:
                        if offer.status!='accepted':
                            offer.status="refused"
                            refuse_template = self.env.ref("auction_real_estate.email_template_offer_refused")
                            if refuse_template:
                                refuse_template.send_mail(offer.id, force_send=True)
