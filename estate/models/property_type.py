from odoo import api, fields, models


class PropertyType(models.Model):
    # Model Attributes
    _name = 'estate.property.type'
    _description = 'Property Type Model'
    _order = 'sequence, name asc'

    # SQL Constraints
    _sql_constraints = [
		('check_unique_type', 'UNIQUE(name)', "Property type name must be unique.")
	]

    # Basic Fields
    name = fields.Char(string="Property Type", required=True)
    sequence = fields.Integer(string="Sequence", default=1, help="Used to order property types")

    # Relatinal Fields
    property_ids = fields.One2many('estate.property', 'property_type_id')

    # Computed Fields
    offer_count = fields.Integer(compute='_compute_offer_count')

    # Compute Methods
    @api.depends('property_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.property_ids.offer_ids)
