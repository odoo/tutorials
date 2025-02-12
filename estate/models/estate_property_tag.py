# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyTag(models.Model):
  _name = 'estate.property.tag'
  _description = 'estate property'
  _order = 'name asc'

  name = fields.Char(string='Property Tag', required=True)
  color = fields.Integer(string='Color')


  _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)',
         'Tag names must be unique.')
    ]  
