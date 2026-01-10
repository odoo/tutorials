from odoo import api, fields, models


class warrantyWizardLine(models.TransientModel):
    _name = "warranty.wizard.line"
    _description = "warranty Line to Select Warranty"

    wizard_id = fields.Many2one("warranty.wizard", string="Wizard")
    product_id = fields.Many2one("product.product", string="Product")
    sale_order_line_id = fields.Many2one("sale.order.line", string="Sale order Line")
    warranty_id = fields.Many2one("product.warranty", string="Warranty")

    validity_year = fields.Integer(
        string="Validity Year", related="warranty_id.validity_year", readonly=True
    )

    warranty_end_date = fields.Date(
        string="End Date", compute="_compute_warranty_end_date"
    )

    @api.depends("validity_year")
    def _compute_warranty_end_date(self):
        for record in self:
            if record.validity_year:
                record.warranty_end_date = record.warranty_end_date or fields.Date.add(
                    fields.Date.today(), days=365 * record.validity_year
                )
            else:
                record.warranty_end_date = False
