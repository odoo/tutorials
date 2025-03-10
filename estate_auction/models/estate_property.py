from odoo import api, fields, models
from odoo.exceptions import UserError

class estateProperty(models.Model):
    _inherit = "estate.property"

    sell_type = fields.Selection(
        string="Sell Type",
        selection=[
            ("auction", "Auction"),
            ("regular", "Regular"),
        ],
        required=True,
        copy=False,
        default="regular",
    )
    auction_stage = fields.Selection(
        string="Auction Stage",
        selection=[
            ("template","Template"),
            ("auction","Auction"),
            ("offer_accepted","Offer Accepted"),
        ],
        default="template",
        copy=False,
    )
    auction_end_time = fields.Datetime(string="Auction End Time")
    highest_bidder = fields.Many2one(
        comodel_name="res.partner",
        string="Highest Bidder",
        compute='_compute_highest_bidder',
        readonly=True,
    )
    invoice_ids = fields.One2many(string="Invoice", comodel_name="account.move", inverse_name="estate_property_id")
    invoice_count = fields.Integer(string="Invoice Count", compute="_compute_invoice_count")

    def write(self, vals):
        print(self.state)
        if self.auction_stage == 'offer_accepted' and self.state == 'sold':
            raise UserError("You cannot change the auction stage from state sold")
        elif self.auction_stage == 'offer_accepted' and self.state == 'cancelled':
            vals.update({'state': 'new'})
        elif vals.get('auction_stage') == 'offer_accepted':
            if not self.offer_ids:
                vals.update({
                    'state': 'cancelled'
                })
            else:
                winner_template = self.env.ref('estate_auction.mail_template_auction_won')
                losser_template = self.env.ref('estate_auction.mail_template_auction_lost')
                highest_offer = max(self.offer_ids, key=lambda o: o.price, default=False)
                highest_offer.accept_offer()
                if highest_offer.partner_id.email:
                    winner_template.send_mail(self.id)
                for offer in self.offer_ids:
                    if offer != highest_offer:
                        losser_template.send_mail(self.id)
                vals.update({
                    'auction_stage': 'offer_accepted',
                    'auction_end_time': fields.Datetime.now()
                })
        return super().write(vals)

    def action_start_auction(self):
        if self.auction_end_time:
            if self.auction_end_time<fields.Datetime.now():
                raise UserError("Invalid End Time: Auction end time must be a future date and time.")
            self.auction_stage = 'auction'
        else:
            raise UserError("You will need to set Auction End Time")    

    @api.model
    def _action_close_expired_auctions(self):
        """ Close expired auctions """
        expired_properties = self.search([
            ('sell_type', '=', 'auction'),
            ('auction_stage', '=', 'auction'),
            ('auction_end_time', '<', fields.Datetime.now())
        ])
        for property in expired_properties:
            property.write({'auction_stage': 'offer_accepted'})            

    @api.depends('best_price')
    def _compute_highest_bidder(self):
        for property in self:
            if property.offer_ids:
                highest_offer = max(property.offer_ids, key=lambda offer: offer.price, default=False)
                property.highest_bidder = highest_offer.partner_id if highest_offer else False
            else:
                property.highest_bidder = False        

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = len(record.invoice_ids)
