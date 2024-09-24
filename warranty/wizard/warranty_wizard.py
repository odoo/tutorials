from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from odoo import models, Command, fields, api


class WarrantyWizard(models.TransientModel):
    _name = "warranty.wizard"
    _description = "Warranty Management Wizard"

    warranty_line_ids = fields.One2many(
        "warranty.wizard.line", "wizard_id", string="Warranty Lines"
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        sale_order = self.env["sale.order"].browse(self.env.context.get("active_id"))

        lines = []
        for line in sale_order.order_line:
            if line.product_id.is_warranty_available:
                # Check if warranty is available
                lines.append(
                    (
                        0,
                        0,
                        {
                            "product_id": line.product_id.id,
                        },
                    )
                )
        res["warranty_line_ids"] = lines
        return res

    def apply_warranties(self):

        active_id = self.env.context.get("active_id")
        sale_order = self.env["sale.order"].browse(active_id)

        for line in self.warranty_line_ids:
            
            if line.year:
                for record in sale_order.order_line:
                    if record.product_id == line.product_id:
                         price  = (record.price_subtotal * line.year.percentage)/100
                
                sale_order.order_line = [
                        Command.create(
                            {
                                "name": "Extended Warranty",
                                "order_id": sale_order.id,
                                "product_id": line.year.product_id.id,
                                "product_uom": 1,
                                "product_uom_qty": 1,
                                "price_unit": price,
                                "tax_id": None,
                            }
                        )
                    ]       
               
            
            
            
            
class WarrantyWizardLine(models.TransientModel):
    _name = "warranty.wizard.line"
    _description = "Warranty Wizard Line"

    year = fields.Many2one("add.warranty")
    end_date = fields.Date(string="End Date")
    product_id = fields.Many2one("product.product", string="Product")
    wizard_id = fields.Many2one("warranty.wizard", string="Wizard")

    @api.onchange("year")
    def _onchange_year(self):
        if self.year:
            self.end_date = date.today() + relativedelta(years=self.year.period)
        else:
            self.end_date = False
