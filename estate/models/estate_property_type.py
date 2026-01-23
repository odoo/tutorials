from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "An estate property type model"
    _order = "name asc"

    # === FIELDS ===#

    name = fields.Char(
        required=True)
    property_ids = fields.One2many(
        "estate.property",
        "property_type_id")
    sequence = fields.Integer(
        'Sequence',
        default=1)
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
    )
    offer_count = fields.Integer(
        compute='_compute_offer_count',
        string="Offers",
    )

    _check_name = models.Constraint(
        'unique(name)',
        'The property type name must be unique!',
    )

    # === COMPUTE METHODS ===#

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
