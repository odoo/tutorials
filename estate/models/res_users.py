# -*- coding: utf-8 -*-

from odoo import models, fields


class EstateResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        'estate_property',
        'salesperson',
        string='Properties',
    )

