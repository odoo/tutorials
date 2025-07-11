from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = "name"
    _sql_constraints = [
        ('unique_property_type_name', 'UNIQUE(name)', 'Property type name must be unique.')
    ]
    
    name = fields.Char(string='Property Type', required=True)
    offer_count = fields.Integer(compute="_compute_offer_count")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    property_count = fields.Integer("Property Count", compute="_compute_property_count")
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id", string="Offers")
    
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def _compute_property_count(self):
        for record in self:
            record.property_count = len(record.property_ids)
            