from odoo import fields, models


class View(models.Model):
    _inherit = 'ir.ui.view'

    gallery_type = fields.Selection(selection_add=[('gallery', "Awesome Gallery")])
