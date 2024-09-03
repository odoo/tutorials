from odoo import fields, models
from odoo.exceptions import UserError


class addOfferproperteis(models.TransientModel):
    _name = "add.offer"
    _description = "Add offer to properties"

    price = fields.Integer(required=True)
    validity = fields.Integer()
    buyer_id = fields.Many2one(
        "res.partner", string="buyer", copy=False, ondelete="cascade"
    )

    property_ids = fields.Many2many(
        "estate.property", string="Property ID", ondelete="cascade"
    )

    def add_offer_properties(self):
        active_ids = self.env.context.get("active_ids", [])

        if not active_ids:
            raise UserError("No property selected")
        properties = self.env["estate.property"].browse(active_ids)
        for props in properties:
            self.env["estate.property.offer"].create(
                {
                    "price": self.price,
                    "partner_id": self.buyer_id.id,
                    "property_id": props.id,
                }
            )
