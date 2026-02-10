from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "estate property types"
    _order = 'name'
    # _rec_name = 'id'
    # _rec_names_search = ['sequence']

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type')
    sequence = fields.Integer()
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')
    _uniq_tag_name = models.Constraint(
        "unique(name)",
        "A Property Type already exist, Propert type should be unique.",
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
