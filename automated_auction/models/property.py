from odoo import _, api, fields, models
from odoo.exceptions import UserError


class Property(models.Model):
    _inherit = 'estate.property'

    property_auction_type = fields.Selection(
        string="Auction Type",
        help="Automated auction\n"
             "Regular auction",
        selection=[
            ('auction', "Auction"),
            ('regular', "Regular"),
        ],
        required=True,
        default='regular',
    )
    start_time = fields.Datetime()
    end_time = fields.Datetime()
    highest_offer_bidder = fields.Many2one('res.partner', compute="_compute_highest_bidder", readonly=True)

    @api.depends('offer_ids.price')
    def _compute_highest_bidder(self):
        for record in self:
            highest_offer = max(record.offer_ids, key=lambda o: o.price, default=None)
            record.highest_offer_bidder = highest_offer.partner_id if highest_offer else False

    def action_start_auction(self):
        self.ensure_one()
        if not self.end_time:
            raise UserError(_("Please select Auction End Time first"))
        self.start_time = fields.Datetime.now()
