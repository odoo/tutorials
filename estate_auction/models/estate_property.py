from odoo import api, fields, models
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = "estate.property"

    auction_start = fields.Datetime(string="Auction Start Time")
    auction_end = fields.Datetime(string="Auction End Time")
    auction_started = fields.Boolean(string="Auction started", default=False)
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

    invoice_ids = fields.One2many(string="Invoice", comodel_name="account.move", inverse_name="estate_property_id")
    invoice_count = fields.Integer(string="Invoice Count", compute="_compute_invoice_count")

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for property in self:
            property.invoice_count = len(property.invoice_ids)

    @api.onchange('sale_type')
    def _onchange_sale_type(self):
        for property in self:
            if property.sale_type == 'regular' and property.auction_state != 'template':
                raise UserError("You can not switch to sale type 'regular' after starting the auction")

    @api.constrains('auction_end')
    def _check_auction_end_date(self):
        for record in self:
            if record.sale_type == 'auction' and record.auction_end and record.auction_end <= fields.Datetime.now():
                raise UserError("Auction end time must be in the furture.")

    def action_start_auction(self):
        for property in self:
            if not property.auction_end:
                raise UserError("Auction end time must set before starting the auction.")
            property.auction_started = True
            property.auction_state = 'auction'
            property.auction_start = fields.Datetime.now()
        return True

    def _cron_check_expired_auction(self):
        print("In Cron")
        currentDate = fields.Datetime.now()
        domain = [
            ("auction_state", "=", "auction"),
            ("auction_end", "<=", currentDate),
        ]
        expired_properties = self.search(domain)
        for property in expired_properties:
            offers = property.property_offer_ids.sorted('price', reverse=True)
            highest_offer = offers[0]
            highest_offer.state = 'accepted'
            property.write({
                "highest_bid" : highest_offer.price,
                "highest_bidder_id" : highest_offer.partner_id.id,
                "buyer_id": highest_offer.partner_id.id,
                "auction_state": "sold",
                "state": "offer_accepted",
            })
            template = self.env.ref("estate_auction.email_template_offer_accepted")
            template.send_mail(highest_offer.id, force_send=True)
            lower_offers = offers[1:]
            for offer in lower_offers:
                offer.state = 'refused'
                template = self.env.ref("estate_auction.email_template_offer_refused")
                template.send_mail(offer.id, force_send=True)
            property.auction_state = 'sold'
        return True
