# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_pricelist_on = fields.Boolean(string="Pricelist Available")
    
    pricelist_item_ids = fields.One2many(comodel_name='product.pricelist.item', 
        inverse_name='product_tmpl_id', 
        string="Pricelist Rules")

    pricelist_id = fields.Many2one(comodel_name='product.pricelist',
        related='pricelist_item_ids.pricelist_id',
        string="Pricelist",
        store=True
    )
