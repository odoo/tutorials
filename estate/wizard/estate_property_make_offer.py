from odoo import fields,models


class EstateWizardMultiOffer(models.TransientModel):
    _name = "estate.property.make.offer"
    _description = "Estate Property Make Offer Wizard"

    price = fields.Float(string="Offer Price", required=True)
    validate = fields.Integer(string="Validity (days)", default=7, required=True)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)

    def make_offer(self):
        for property in self.env.context.get("active_ids"):
            try:
                self.env["estate.property.offer"].create(
                    {
                        "partner_id": self.partner_id.id,
                        "price": self.price,
                        "validate": self.validate,
                        "property_id": property,
                    }
                )
            except Exception:
                continue
