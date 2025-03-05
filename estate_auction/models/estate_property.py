from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    selling_mode = fields.Selection(
        selection=[
        ('regular', "Regular"),
        ('auction', "Auction"),
    ], default='regular', required=True)
    auction_end_time = fields.Datetime(string="End Time")
    highest_offer = fields.Float(string="Highest Offer", compute='_compute_highest_offer', readonly=True)
    highest_bidder = fields.Many2one('res.partner', string="Highest Bidder", compute='_compute_highest_offer', readonly=True)
    auction_stage = fields.Selection(
        selection=[
        ('01_template', "Template"),
        ('02_auction', "Auction"),
        ('03_sold', "Sold")
    ], string="Auction Stage", default='01_template', tracking=True)

    @api.depends('offer_ids.price', 'offer_ids.partner_id')
    def _compute_highest_offer(self):
        for record in self:
            if record.offer_ids:
                highest_offer = max(record.offer_ids, key=lambda o: o.price, default=None)
                record.highest_bidder = highest_offer.partner_id if highest_offer else False
                record.highest_offer = highest_offer.price if highest_offer else 0.0
            else:
                record.highest_bidder = False
                record.highest_offer = 0.0

    def action_start_auction(self):
        """Start the auction process for this property"""
        self.ensure_one()
        if self.state in ['sold', 'cancelled']:
            raise UserError(_("Cannot start auction for sold or cancelled properties."))
        
        if not self.selling_mode == 'regular':
            raise UserError(_("This property is not marked for auction."))
            
        if not self.auction_end_time:
            raise UserError(_("Please set an end time for the auction."))
            
        self.auction_stage = 'auction'
        return True
        
    def check_auction_status(self):
        """
        Cron job to check if auctions have ended and process them
        This will run every 5 minutes
        """
        current_time = fields.Datetime.now()
        auction_properties = self.search([
            ('selling_mode', '=', 'auction'),
            ('state', 'in', ['new', 'offer_received']),
            ('auction_end_time', '<=', current_time)
        ])
        
        for prop in auction_properties:
            if prop.offer_ids:
                # Find the highest offer
                highest_offer = max(prop.offer_ids, key=lambda o: o.price)
                
                # Accept the highest offer
                highest_offer.action_accept()
                
                # Log the automatic acceptance
                prop.message_post(
                    body=_("Auction ended. Highest offer (%.2f) from %s was automatically accepted.") % 
                    (highest_offer.price, highest_offer.partner_id.name)
                )
            else:
                # No offers received, mark as auction ended
                prop.write({
                    'state': 'cancelled',
                    'auction_stage': '03_sold'  # Using the sold stage even though it's cancelled
                })
                prop.message_post(body=_("Auction ended with no offers."))
