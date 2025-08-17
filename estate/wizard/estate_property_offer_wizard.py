from odoo import fields, models

class EstatePropertyOfferWizard(models.TransientModel):
    _name = "estate.property.offer.wizard"
    _description = "wizard to add offers in selected property"

    price = fields.Float("Offer Price", required=True)
    validity = fields.Integer("Validity", required=True, default=7)
    partner_id = fields.Many2one("res.partner", "Buyer", required=True)

    def action_create_offer(self):

        # collect all the selected properties
        active_ids = self._context.get("active_ids")
        # search it in model and convert it to recordset
        property_ids = self.env["estate.property"].browse(active_ids)

        if not property_ids:
            return {"type": "ir.actions.act_window_close"}

        vals_list = []
        for record in property_ids:
            vals_list.append({
                "price": self.price,
                "validity": self.validity,
                "partner_id": self.partner_id.id,
                "property_id": record.id,
            })

        self.env["estate.property.offer"].create(vals_list)

        return {"type": "ir.actions.act_window_close"}
