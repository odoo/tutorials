# -*- coding: utf-8 -*-
from odoo import fields, models


class ActWindowView(models.Model):
    _inherit = 'ir.actions.act_window.view'

    .Selection(selection_add=[
        ('gallery', "Awesome Gallery")
    ],  ondelete={'gallery': 'cascade'})
