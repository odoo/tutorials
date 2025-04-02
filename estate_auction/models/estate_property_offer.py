from odoo import api, fields, models
from odoo.exceptions import ValidationError

class EstatePropertyOffer(models.Model):
    _inherit = 'estate.property.offer' 

    isAuction=fields.Boolean(string="Is Auction",  compute="_compute_is_auction", default=True)

    @api.depends("property_id.bid_type")
    def _compute_is_auction(self):
        if self.property_id.bid_type=="auction":
            self.isAuction=True
            # print(self.isAuction)
        else:
            self.isAuction=False
            self.property_id.auction_end_time=False

    def accept_offer(self):
        for record in self:
            if record.property_id.bid_type == "auction":
                raise ValidationError(("You cannot manually accept an offer for an auction property. The highest bid will be accepted automatically when the auction ends."))
        return super().accept_offer()
