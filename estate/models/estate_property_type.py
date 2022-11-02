from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name asc"

    sequence = fields.Integer(
        string='Sequence',
        default=1,
        help='Sequence for sorting',
    )
    name = fields.Char(required=True)
    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="property_type_id",
        string="Properties",
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_type_id",
        string="Offers",
    )

    offer_count = fields.Integer(
        compute='_compute_offer_count',
        store=True,
    )

    _unique_constraints = models.Constraint(
        definition='UNIQUE(name)',
        message='The property type name must be unique',
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
