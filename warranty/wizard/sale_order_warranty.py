from odoo import _, api, fields, models
from datetime import timedelta
from odoo.exceptions import ValidationError

class SaleOrderWarranty(models.TransientModel):
    _name = "sale.order.warranty"
    _description = "Warranty Wizard"

    sale_order_id = fields.Many2one("sale.order", required=True, default=lambda self: self.env.context.get('active_id'))
    product_id = fields.Many2one("product.template", string="Product", domain=[('has_warranty', '=', True)])
    year = fields.Integer("Year", default=1)
    end_date = fields.Date("End Date", compute="_compute_end_date")

    @api.depends('year')
    def _compute_end_date(self):
        for record in self:
            if record.year < 0:
                raise ValidationError(_("Warranty year cannot be negative"))
            if record.year:
                record.end_date = fields.Date.today() + timedelta(days = record.year * 365)
                print(record.end_date)
            else:
                record.end_date = False

    def _prepare_warranty_line_values(self):
        self.ensure_one()
        warranty_config = self.env['warranty'].search([('product_id', '=', self.product_id.id)])
        if not warranty_config:
            raise ValidationError(_("No warranty Configuration found for the selected product"))


    def action_apply_warranty(self):
        self.ensure_one()

