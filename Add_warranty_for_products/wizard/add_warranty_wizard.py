from odoo import models, fields, api
from datetime import timedelta


class WarrantyConfigurationWizard(models.TransientModel):
    _name = 'warranty.configuration.wizard'
    _description = 'Warranty Configuration Wizard'

    order_id = fields.Many2one('sale.order', string="Sales Order")
    warranty_line_ids = fields.One2many(
        'warranty.configuration.wizard.line',
        'wizard_id',
        string="Warranty Lines"
    )

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        order = self.env['sale.order'].browse(self.env.context.get("default_order_id", False))
        if order:
            defaults.update({
                "order_id": order.id,
                "warranty_line_ids": [
                    (0, 0, {"order_line_id": line.id})
                    for line in order.order_line
                    if line.product_id.is_warranty_available
                ]
            })
        return defaults

    def action_add_warranty(self):
        for line in self.warranty_line_ids.filtered(lambda l: l.order_line_id and l.warranty_id):
            product = line.order_line_id.product_id
            warranty_product = line.warranty_id.product_id
            warranty_price = (line.order_line_id.price_unit / 100) * line.warranty_id.percentage
            warranty_description = f"Warranty for {product.name} - {line.warranty_id.name} (Ends: {line.end_date})"

            existing_line = self.order_id.order_line.filtered(
                lambda ol: ol.linked_order_line_id == line.order_line_id
            )
            if existing_line:
                existing_line.write({
                    "product_id": warranty_product.product_variant_id.id,
                    "name": warranty_description,
                    "price_unit": warranty_price,
                })
            else:
                self.env["sale.order.line"].create({
                    "order_id": self.order_id.id,
                    "product_id": warranty_product.product_variant_id.id,
                    "name": warranty_description,
                    "product_uom_qty": line.order_line_id.product_uom_qty,
                    "price_unit": warranty_price,
                    "linked_order_line_id": line.order_line_id.id,
                })


class WarrantyConfigurationWizardLine(models.TransientModel):
    _name = 'warranty.configuration.wizard.line'
    _description = 'Warranty Configuration Wizard Line'

    wizard_id = fields.Many2one('warranty.configuration.wizard', ondelete="cascade")
    order_line_id = fields.Many2one(
        'sale.order.line',
        string="Product",
        domain="[('order_id', '=', wizard_id.order_id), ('product_id.is_warranty_available', '=', True)]",
        required=True
    )
    warranty_id = fields.Many2one('warranty.configuration', string="Warranty")
    end_date = fields.Date(string="End Date", compute="_compute_end_date", store=True)

    @api.depends('warranty_id')
    def _compute_end_date(self):
        today = fields.Date.today()
        for line in self:
            line.end_date = (
                today + timedelta(days=line.warranty_id.warranty_period * 365)
                if line.warranty_id else False
            )


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('order_line')
    def _onchange_order_line(self):
        base_lines = self.order_line.filtered(lambda l: not l.linked_order_line_id)
        self.order_line = self.order_line.filtered(
            lambda l: not l.linked_order_line_id or l.linked_order_line_id.id in base_lines.ids
        )

    has_warranty_available = fields.Boolean(
    string="Has Warranty Available",
    compute='_compute_has_warranty_available',
    store=True)

    @api.depends('order_line.product_id.is_warranty_available')
    def _compute_has_warranty_available(self):
        for order in self:
            order.has_warranty_available = any(
                line.product_id.is_warranty_available
                for line in order.order_line
            )
