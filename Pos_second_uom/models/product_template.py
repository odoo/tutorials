from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    uom_category_id = fields.Many2one(
        comodel_name='uom.uom',
        string='UoM Category',
        related='uom_id.category_id',
        store=True
    )

    pos_secondary_uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string='Secondary Unit of Measure',
        domain="[('category_id', '=', uom_category_id), ('id', '!=', uom_id)]"
    )

    @api.onchange('uom_id')
    def _onchange_uom_id(self):
        self.pos_secondary_uom_id = False


class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = ['product.product']

    @api.model
    def _load_pos_data_fields(self, config_id):
        return super()._load_pos_data_fields(config_id) + ['pos_secondary_uom_id']
