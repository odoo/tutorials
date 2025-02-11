from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(string="Type Name")
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")

    _order = "name"

    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(compute='_compute_offer_count')
    sequence = fields.Integer()


    # -------------------------------------------------------------------------
    # SQL CONSTRAINTS QUERIES
    # -------------------------------------------------------------------------

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'The property type name must be unique.')
    ]


    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
