# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CatalogFields(models.Model):
    _name = 'catalog.fields'
    _description = "Catalog Fields"
    
    catalog_fields_line_id = fields.Many2one(comodel_name='catalog.catalog')
    sequence = fields.Integer(default=1)
    fields = fields.Selection(
        selection=[
            ('name', "Name"),
            ('lst_price', "Price"),
            ('image_1920', "Image"),
            ('qty_available', "Quantity On Hand"),
        ],
        string="Fields"
    )
