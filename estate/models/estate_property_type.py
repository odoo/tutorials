from odoo import fields, models


class PropertyType(models.Model):
    _name='estate.property.type'
    _description='Property Type'
    _order= 'name asc'

    name=fields.Char(string="Name", required=True)
    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='property_type_id')
    sequence = fields.Integer('Sequence',
        default=1,
        help="Used to order property types based on sequence.",
        copy=False  # Prevents sequence duplication when duplicating records
    )

    offer_count = fields.Integer(
        string="Offers Count",
        compute='_compute_offer_count'
    )

    _sql_constraints = [
        ('uniq_name', 'unique(name)' ,"Property Type Name should be unique"),
    ]

    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.property_ids.offer_ids)
