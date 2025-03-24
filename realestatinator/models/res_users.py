# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Users(models.Model):
	_inherit = 'res.users'
	
	property_ids = fields.One2many('estate_property', 'sales_person', string='Properties')
