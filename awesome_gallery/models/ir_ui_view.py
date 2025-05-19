# -*- coding: utf-8 -*-
from odoo import fields, models


class View(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection(selection_add=[('gallery', "Awesome Gallery")])

    def _get_view_info(self):
        view_info = {'gallery': {'icon': 'fa fa-picture-o'}} | super()._get_view_info()
        return view_info
