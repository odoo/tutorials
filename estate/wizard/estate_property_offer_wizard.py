from odoo import api, fields, models


class EstateOfferWizard(models.TransientModel):
    _name = "estate.property.offer.wizard"
    property_ids = fields.Many2many("estate.property", required=True)
    validity = fields.Integer(default=7)
    partner_id = fields.Many2one("res.partner")
    price = fields.Float()

    # getting default values
    @api.model_create_multi
    def default_get(self, fields):
        res = super(EstateOfferWizard, self).default_get(fields)
        active_ids = self.env.context.get("active_ids", [])
        if active_ids:
            print()
            print()
            print(active_ids)
            print()
            print()
            res.update({"property_ids": [(6, 0, active_ids)]})
        return res

    def make_offer(self):
        for property in self.property_ids:
            self.env["estate.property.offer"].create(
                {
                    "property_id": property.id,
                    "price": self.price,
                    "validity": self.validity,
                    "partner_id": self.partner_id.id,
                }
            )
        return {"type": "ir.actions.act_window_close"}
