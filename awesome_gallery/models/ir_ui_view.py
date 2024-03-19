# -*- coding: utf-8 -*-
from odoo import fields, models


class View(models.Model):
    _inherit = 'ir.ui.views'

    type = fields.Selection(selection_add=[('gallery', "Awesome Gallery")])
