from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class SaleOrderWarranty(models.TransientModel):
    _name = "sale.order.warranty"
    _description = "Warranty Wizard"

    sale_order_id = fields.Many2one("sale.order", required=True, default=lambda self: self.env.context.get('active_id'))
    product_id = fields.Many2one("product.template", string="Product", domain=[('has_warranty', '=', True)])
    warranty_id = fields.Many2one('warranty.config', domain="[('product_id', '=', product_id)]", required=True)
    end_date = fields.Date("End Date", compute="_compute_end_date")

    @api.depends('warranty_id')
    def _compute_end_date(self):
        for record in self:
            if record.warranty_id:
                record.end_date = fields.Date.today() + relativedelta(years = record.warranty_id.year)
            else:
                record.end_date = False

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.warranty_id = False

            warranties = self.env['warranty.config'].search([('product_id', '=', self.product_id.id)])
            if not warranties:
                return {
                    'warning': {
                        'title': _("No warranty Configurations"),
                        'message': _("No warranty configurations found for this product. Configure warranties before adding it.")
                    }
                }
        else:
            self.warranty_id = False

    def _prepare_warranty_line_values(self):
        self.ensure_one()
        if not self.warranty_id:
            raise ValidationError(
                _("No warranty selected. Please select a warranty configuration for the product '%(name)s'.", name=self.product_id.name)
            )

        warranty_config = self.warranty_id
        if warranty_config.product_id != self.product_id:
            raise ValidationError(
                _("The selected warranty configuration does not match the product '%(name)s'.", name=self.product_id.name)
            )

        sale_line = self.sale_order_id.order_line.filtered(lambda list: list.product_id.product_tmpl_id == self.product_id)
        if not sale_line:
            raise ValidationError(
                _("The product '%(name)s' is not present in the sale order lines. Please add the product to the order before applying a warranty.", name=self.product_id.name)
            )

        if sale_line.price_unit:
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
            'tax_id':False,
        }

    def action_apply_warranty(self):
        self.ensure_one()
        existing_warranty_line = self.sale_order_id.order_line.filtered(
            lambda line: line.product_id.product_tmpl_id == self.product_id and "Extended Warranty" in line.name
        )
        if existing_warranty_line:
            raise ValidationError(
                _("A warranty has already been added for the product '%(name)s'.", name=self.product_id.name)
            )
        else:
            warranty_line_vals = self._prepare_warranty_line_values()
            self.env['sale.order.line'].create(warranty_line_vals)
