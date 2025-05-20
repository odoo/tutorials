from odoo import fields, models


class estatePropertyTag(models.Model):
	_name="estate.property.tag"
	_description = "typie, co ty paczysz?"
	name = fields.Char(required=True)
