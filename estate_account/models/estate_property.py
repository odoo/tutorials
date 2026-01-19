from odoo import models, Command, exceptions, _


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        for record in self:
            if record.state == "cancelled":
                raise exceptions.UserError(_("Properties which are Cancelled cannot be Sold"))

            if record.salesperson:
                if record.salesperson.has_group("sales_team.group_sale_manager"):
                    admin_fee = 200
                else:
                    admin_fee = 100
            else:
                admin_fee = 50

            self.env["account.move"].create({
                "partner_id": record.customer.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({
                        "name": record.name,
                        "quantity": 1,
                        "price_unit": record.selling_price * 0.6,
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": admin_fee,
                    }),
                ],
            })

        return super().action_sold_property()
