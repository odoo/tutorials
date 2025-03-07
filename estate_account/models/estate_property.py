from odoo import api, fields, models,Command

class EstateProperty(models.Model):
    _description = "Estate Account property Model"
    _inherit="estate.property"

    invoice_ids = fields.One2many(
        string="Invoice",
        help="Invoices related to the property.",
        comodel_name="account.move",
        inverse_name="estate_property_id"
    )
    invoice_count = fields.Integer(
        string="Invoice Count",
        help="Number of invoices related to the property.",
        compute="_compute_invoice_count"
    )
    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = len(record.invoice_ids)

    def action_mark_property_sold(self):
        self.check_access('write')

        self.env["account.move"].sudo().create({
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "estate_property_id": self.id,
            "invoice_line_ids": [
                Command.create({
                    "name": self.name,
                    "quantity": 1,
                    "price_unit": self.selling_price,
                }),
                Command.create({
                    "name": "Property Sale Commission",
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06
                }),
                Command.create({
                    "name": "Additional Fees",
                    "quantity": 1,
                    "price_unit": 100.00
                })
            ],
        })
        return super().action_mark_property_sold()
