from odoo import fields, models

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    auction_type = fields.Selection([
        ('regular', 'Regular'),
        ('auction', 'Auction'),
    ], string='Auction Type', default='regular')

    auction_end_time = fields.Datetime(string='End Time')
    highest_offer = fields.Float(string='Highest Offer', readonly=True)
    highest_bidder_id = fields.Many2one('res.partner', string='Highest Bidder', readonly=True)
  
    def action_start_auction(self):
        return
    
    def open_status(self):
        return
