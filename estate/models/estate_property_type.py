# -*- coding: utf-8 -*-
from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate_property_type'
    _description = 'Real Estate Property Type'

    name = fields.Char(required=True)

