from odoo import models,fields,api

class ProductTemplate(models.Model):
    _inherit = ['product.template']

    def _get_default_second_uom(self):
        return self.env.ref('uom.product_uom_dozen')

    uom_category_id = fields.Many2one('uom.category', string='UoM Category', related="uom_id.category_id")
    second_uom_id = fields.Many2one(string="Second UoM", comodel_name="uom.uom", help="It helps in choosing product in second UoM", domain="[('category_id', '=', uom_category_id), ('id', '!=', uom_id)]", default=_get_default_second_uom, required=True)

    @api.onchange('uom_id')
    def _onchange_uom_id(self):
        """
        Update second_uom default value dynamically whenever uom_id changes.
        """
        if self.uom_id:
            domain = [('category_id', '=', self.uom_id.category_id.id), ('id', '!=', self.uom_id.id)]
            second_uom_id = self.env['uom.uom'].search(domain, limit=1)
            self.second_uom_id = second_uom_id.id if second_uom_id else False
        else:
            self.second_uom = False

class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = ['product.product', 'pos.load.mixin']

    @api.model
    def _load_pos_data_fields(self, config_id):
        return super()._load_pos_data_fields(config_id) + ['second_uom_id']
