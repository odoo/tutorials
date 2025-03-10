from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "  Real Estate Property Type"
    _order = 'name'

    name = fields.Char(string="Property Type", required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    sequence = fields.Integer('Sequence', default=1, help="Used to order Property type. ")

    _sql_constraints = [
        ("unique_type_name", "UNIQUE(name)", "The property type name must be unique.")
    ]

    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="offers")
    offer_count = fields.Integer(compute = "_compute_offer_count", string="Offers")

    # count offer for display at star button
    # @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
