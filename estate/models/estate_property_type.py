from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Record types of the property"
    _order = 'sequence, name'
    # constrain
    _sql_constraints = [
        ('unique_type', 'UNIQUE (name)', "The type name must be unique.")
    ]

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence", default=1)
    offer_count = fields.Integer(string="Total Offers", compute='_compute_offer_count')

    # relational fields
    property_ids = fields.One2many(
        comodel_name='estate.property',
        inverse_name='property_type_id',
        string="Property Details"
    )
    offer_ids = fields.One2many(string="Offers", comodel_name='estate.property.offer', inverse_name='property_type_id')

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for type in self:
            type.offer_count = len(type.offer_ids)
