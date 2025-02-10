from odoo import models, fields,api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Property Type"

    name = fields.Char(string="Type", required=True)

    property_ids=fields.One2many('estate.property','property_type_id')
    offer_ptype_ids = fields.One2many(
        "estate.property.offer", "property_type_id", string="Offers"
    )

    offer_count=fields.Integer(string="Offer Counts",compute='_compute_offer_count')

    @api.depends("offer_ptype_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count=len(record.offer_ptype_ids)

    _order="name"
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    _sql_constraints = [
        ('unique_property_type_name', 'UNIQUE(name)', 'Property type name must be unique!')
    ]
