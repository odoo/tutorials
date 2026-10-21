from odoo import api, models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer(string="Sequence", default=1)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _name_unique = models.Constraint(
        'unique (name)',
        'This type already exists'
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            if o := record.offer_ids:
                record.offer_count = len(o)
            else:
                record.offer_count = 0
