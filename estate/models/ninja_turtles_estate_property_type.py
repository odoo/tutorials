from odoo import fields, models, api


class NinjaTurtlesEstatePropertyType(models.Model):
    _name = "ninja.turtles.estate.property.type"
    _description = "Ninja Turtle Estate for faster Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'Property type name must be unique.')
    ]

    property_ids = fields.One2many("ninja.turtles.estate",
                                   "property_type_id",
                                   string="Properties")

    sequence = fields.Integer('Sequence', default=1)

    offer_ids = fields.One2many(
        "ninja.turtles.estate.property.offer",
        "property_type_id",
        string="Offers",
    )

    offer_count = fields.Integer(
        compute="_compute_offer_count",
        string=" Number of Offers",
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
