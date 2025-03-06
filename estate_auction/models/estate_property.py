from odoo import api, fields, models
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = "estate.property"

    auction_start = fields.Datetime(string="Auction Start Time")
    auction_end = fields.Datetime(string="Auction End Time")
    timer_running = fields.Boolean(string="Timer Running", default=False)
    highest_bid = fields.Float(string="Highest Bid", readonly=True)
    highest_bidder_id = fields.Many2one(comodel_name="res.partner", string="Highest Bidder", readonly=True)

    sale_type = fields.Selection(string= "Sale Type",
        selection=[
            ('auction', 'Auction'),
            ('regular', 'Regular')
        ],
        default= 'regular',
        tracking= True,
        store= True 
    )

    auction_state = fields.Selection(string= "Auction State",
        selection=[
            ('template','Template'),
            ('auction','Auction'),
            ('sold','Sold')
        ],
        default='template',
        tracking= True
    )
    
    @api.constrains('auction_end')
    def _check_auction_end_date(self):
        for record in self:
            if record.sale_type == 'auction' and record.auction_end and record.auction_end <= fields.Datetime.now():
                raise UserError("Auction end time must be in the furture.")    
    
    def action_start_acution(self):
        print("Hello")
        self.timer_running = True
