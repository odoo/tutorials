from odoo import _, api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


class SaleOrderWarranty(models.TransientModel):
    _name = "sale.order.warranty"
    _description = "Warranty Wizard"

    sale_order_id = fields.Many2one("sale.order", required=True, default=lambda self: self.env.context.get('active_id'))
    product_id = fields.Many2one("product.template", string="Product", domain=[('has_warranty', '=', True)])
    year_id = fields.Many2one('warranty', string="Year")
    year = fields.Integer("Year", default=1)
    end_date = fields.Date("End Date", compute="_compute_end_date")

    @api.depends('year')
    def _compute_end_date(self):
        for record in self:
            if record.year < 0:
                raise ValidationError(_("Warranty year cannot be negative"))
            if record.year:
                record.end_date = fields.Date.today() + relativedelta(years = record.year)
            else:
                record.end_date = False

    def _prepare_warranty_line_values(self):
        self.ensure_one()
        warranty_config = self.env['warranty'].search([
                ('product_id', '=', self.product_id.id),
                ('year', '=', self.year)
            ], limit=1)
        if not warranty_config:
            raise ValidationError(
                _("No warranty configuration found for the selected product '%(product)s' for '%(years)d' years."
                  "Please configure a warranty for this product in the Warranty Configuration.", product=self.product_id.name, years=self.year))

        sale_line = self.sale_order_id.order_line.filtered(lambda list: list.product_id.product_tmpl_id == self.product_id)
        if sale_line:
            base_price = sale_line.price_unit
        else:
            base_price = self.product_id.list_price
        warranty_price = base_price * (warranty_config.percentage / 100)
        return{
                'order_id': self.sale_order_id.id,
                'product_id': self.product_id.product_variant_id.id,
                'name': f'Extended Warranty for {self.product_id.name} - End Date: {self.end_date}',
                'price_unit': warranty_price,
                'product_uom_qty': 1.0,
                'warranty_end_date': self.end_date,
        }

    def action_apply_warranty(self):
        self.ensure_one()
        warranty_line_vals = self._prepare_warranty_line_values()
        self.env['sale.order.line'].create(warranty_line_vals)
        return{
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': self.sale_order_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
