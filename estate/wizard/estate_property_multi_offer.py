import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class EstatePropertyMultiOffer(models.TransientModel):
    _name = "estate.property.multi.offer"
    _description = "Estate property multi offer wizard"
    
    price = fields.Integer(string="Price", required=True)
    validity = fields.Integer(string="Validity", required=True, default=7)
    buyer_id = fields.Many2one(string="Buyer", comodel_name="res.partner")

    def action_make_offer(self):
        for property_id in self.env.context.get("active_ids"):
            try:
                self.env["estate.property.offer"].create({
                    "price": self.price,
                    "validity": self.validity,
                    "partner_id": self.buyer_id.id,
                    "property_id": property_id
                })
            except Exception as err:
                _logger.warning(err)
        return True
