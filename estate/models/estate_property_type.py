from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    sequence = fields.Integer(string="Sequence")
    # Basic Fields
    name = fields.Char(required=True)
    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], string='Status', default='active', required=True)
    description = fields.Text(string="Description")
    # One2Many
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_type_id',
        string='Offers',
    )
    offer_count = fields.Integer(string='Number of Offers', compute='_compute_offer_count')
    # SQL Constraints
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'The property type name must be unique.'),
    ]

    @api.depends("property_ids.offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
