from odoo import fields, models, api

class InheritedProductTemplate(models.Model):
    _inherit= "sale.order.line"
    
    is_kit_product = fields.Boolean(
        string="Is the product is a kit?",
        related='product_template_id.is_kit',
        depends=['product_id']
    )
    
    prev_filled_unit_price=fields.Float()
    
    linked_product_kit_id = fields.Many2one(
        string="Linked product kit Line",
        comodel_name='sale.order.line',
        ondelete='cascade',
        domain="[('order_id', '=', order_id)]",
        copy=False,
        index=True,
    )
    linked_product_kit_ids = fields.One2many(
        string="Linked product kit Lines", comodel_name='sale.order.line', inverse_name='linked_product_kit_id',
    )
    
    is_sub_line= fields.Boolean(
        default=False,
        compute="_compute_is_sub_line",
        store=True
    )
    
    @api.depends('linked_product_kit_id')
    def _compute_is_sub_line(self):
        for record in self:
            if(record.linked_product_kit_id):
                record.is_sub_line= True

    def action_open_add_kit_wizard(self):
        return {
            'type'      : 'ir.actions.act_window',
            'name'      : f'Product: {self.product_id.name}',
            'res_model' : 'product.kit',
            'view_type' : 'form',
            'view_mode' : 'form',
            'target'    : 'new',
            'context': {
                'product_template_id': self.product_template_id.id,
                'sale_order_line_id': self.id
            }
        }
