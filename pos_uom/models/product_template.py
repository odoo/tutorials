from odoo import fields, models, api

class ProductTemplate(models.Model):
   _inherit = 'product.template'

   second_uom_id = fields.Many2one("uom.uom", string="Second UOM")
