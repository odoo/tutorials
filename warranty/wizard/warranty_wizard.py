from odoo import models, fields, api
from datetime import timedelta

class AddWarrantyWizard(models.TransientModel):
    _name = 'add.warranty.wizard'
    _description = 'Add Warranty Wizard'

    sale_order_id = fields.Many2one('sale.order.line', string="Sale Order")
    warranty_line_ids = fields.One2many('add.warranty.line.wizard', 'wizard_id', string="Warranty Lines")

    @api.model
    def default_get(self, fields_list):
        res = super(AddWarrantyWizard, self).default_get(fields_list)
        active_id = self.env.context.get('active_id')
        if active_id:
            sale_order = self.env['sale.order'].browse(active_id)
            warranty_lines = []
            for line in sale_order.order_line:
                if line.product_id.is_warranty_available:
                    warranty_lines.append((0, 0, {
                        'sale_order_line_id': line.id,
                        'product_id': line.product_id.id,
                    }))
            res['sale_order_id'] = sale_order.id
            res['warranty_line_ids'] = warranty_lines
        return res

    def action_add_warranty(self):
        new_order_line_list = []
        
        for record in self:
            sale_order = record.sale_order_id 
            for line in record.warranty_line_ids:
                if line.warranty_config_id.name:
                    new_order_line_list.append(
                        {
                            "order_id": sale_order.id,
                            "name": str(line.warranty_config_id.name)
                            + "/"
                            + str(line.end_date),
                            "price_unit": line.sale_order_line_id.price_subtotal
                            * (line.warranty_config_id.percentage / 100),
                            "product_id": line.warranty_config_id.product_id.id,
                            "warranty_id": line.sale_order_line_id.id,
                            "sequence": line.sale_order_line_id.sequence,
                        }
                    )
        self.env["sale.order.line"].create(new_order_line_list)




class AddWarrantyLineWizard(models.TransientModel):
    _name = 'add.warranty.line.wizard'
    _description = 'Add Warranty Line Wizard'

    wizard_id = fields.Many2one('add.warranty.wizard', string="Wizard")

    sale_order_line_id = fields.Many2one("sale.order.line", string = "Sale Order Line")

    product_id = fields.Many2one('product.product', compute="_compute_product_name", string="Product")
    warranty_config_id = fields.Many2one('warranty.configuration', string="Year", ondelete="cascade")
    end_date = fields.Date(string="End Date", compute="_compute_end_date")

    @api.depends("sale_order_line_id")
    def _compute_product_name(self):
        for record in self:
            if record.sale_order_line_id:
                record.product_id = record.sale_order_line_id.product_id
            else:
                record.product_id = False

    @api.depends('warranty_config_id')
    def _compute_end_date(self):
        for record in self:
            if record.warranty_config_id and record.warranty_config_id.duration:
                record.end_date = fields.Date.today() + timedelta(days=record.warranty_config_id.duration * 365)
            else:
                record.end_date = False
