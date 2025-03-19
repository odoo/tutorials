from odoo import api, fields, models, Command
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"
    
    property_sale_type = fields.Selection(
        selection = [
            ("auction", "Auction"),
            ("regular", "Regular")
        ],
        string="Property Sale Type", default="regular"
    )
    auction_end_time = fields.Datetime(string="Auction End Time", copy=False)
    highest_offer = fields.Float(string="Highest Offer", compute="_compute_highest_offer", readonly=True)
    highest_bidder = fields.Many2one(
        "res.partner", string="Highest Bidder", compute="_compute_highest_offer", readonly=True, copy=False
    )
    auction_state = fields.Selection([
        ('template', 'Template'),
        ('auction', 'Auction Started'),
        ('sold', 'Sold'),
    ], string="Status", default="template")

    invoice_ids = fields.One2many('account.move', 'property_id', string='invoice')
    
    @api.depends("offer_ids.price")
    def _compute_highest_offer(self):
        for property in self:
            highest_offer = max(property.offer_ids.mapped("price"), default=0)
            highest_bidder = property.offer_ids.filtered(lambda offer: offer.price == highest_offer).partner_id

            property.highest_offer = highest_offer
            property.highest_bidder = highest_bidder.id or False
    
    @api.model
    def _cron_update_auction_status(self):
        now = fields.Datetime.now()
        expired_auctions = self.search([
            ('property_sale_type', '=', 'auction'),
            ('auction_state', '=', 'auction'),
            ('auction_end_time', '<', now),
            ('state', 'not in', ['offer_accepted', 'sold', 'cancelled'])
        ])
        
        for property in expired_auctions:
            highest_bid = max(property.offer_ids, key=lambda offer: offer.price, default=None)

            if highest_bid:
                highest_bid.action_accept()
                property.auction_state = 'sold'
                property.message_post(body=f"Auction ended. Sold for {highest_bid.price} to {highest_bid.partner_id.name}.")
            else:
                property.auction_state = 'template'
                property.message_post(body="Auction ended with no offers.")
    
    def action_start_auction(self):
        if not self.auction_end_time:
            raise UserError("You must set an Auction End Time before starting the auction.")
        
        self.auction_state = "auction"
    
    def action_view_invoice(self):
        """Open related invoices when clicking the smart button."""
        invoices = self.env['account.move'].search([
            ('property_id', '=', self.id),
            ('move_type', '=', 'out_invoice'),
        ])
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        if len(invoices) == 1:
            action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
            action['res_id'] = invoices.id
        else:
            action['domain'] = [('id', 'in', invoices.ids)]
        return action
