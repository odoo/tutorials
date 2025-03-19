from odoo import models,fields,api


class ProductTemplate(models.Model):
    _inherit = ['product.template']

    uom_category_id = fields.Many2one('uom.category', string='UoM Category', related="uom_id.category_id")
    second_uom_id = fields.Many2one(string="Second UoM", comodel_name="uom.uom", help="It helps in choosing product in second UoM", domain="[('category_id', '=', uom_category_id), ('id', '!=', uom_id)]")

    @api.onchange('uom_id')
    def _onchange_uom_id(self):
        self.second_uom_id = False

class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = ['product.product']

    @api.model
    def _load_pos_data_fields(self, config_id):
        return super()._load_pos_data_fields(config_id) + ['second_uom_id']
