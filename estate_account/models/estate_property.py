from odoo import fields, models, Command
from odoo.exceptions import AccessError

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_property_status_sold(self):

        if not self.env["account.move"].check_access_rights("create", False):
            try:
                self.check_access_rights("write")
                self.check_access_rule("write")
            except AccessError:
                return self.env["account.move"]
        
        self.env["account.move"].create({
            "partner_id" : self.buyer_id.id,
            "move_type" : "out_invoice",
            "invoice_line_ids" : [
                Command.create({"name" : "6% of Selling Price", "quantity" : 1, "price_unit" : 0.6 * self.selling_price}),
                Command.create({"name" : "Administration Fee", "quantity" : 1, "price_unit" : 100})
            ]
        })

        return super().action_set_property_status_sold()
