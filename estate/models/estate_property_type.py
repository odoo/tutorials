# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class EstatePropertyType(models.Model):
	_name="estate.property.type"
	_description = "Estate Property Type"
	_order="sequence,name"

	name =fields.Char(string="Property Type Name",required=True)
	property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
	sequence = fields.Integer("Sequence", default=1, help="Used to order stages. Lower is better.")

	_sql_constraints = [
        ("unique_property_type_name", "unique(name)", "The property type name must be unique.")
    ]

