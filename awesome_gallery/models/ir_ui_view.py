# -*- coding: utf-8 -*-
from odoo import fields, models


class View(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection(selection_add=[('gallery', "Awesome Gallery")])

    def _get_view_info(self):
        infos = super()._get_view_info()
        infos['gallery'] = {'icon': 'fa fa-image'}
        return infos
