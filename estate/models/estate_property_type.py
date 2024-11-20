# -*- coding: utf-8 -*-
# licence

from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property types"
    # _order = "sequence"

    name = fields.Char('Type', required=True, translate=True)
    description = fields.Text('Type description')