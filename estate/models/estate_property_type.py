from odoo import models, fields, api


class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Estate property type"
    _order = "sequence,name"

    name = fields.Char("Property Type Name", required=True)
    sequence = fields.Integer(default=1, help="Used to order stages. Lower is ranked higher.")
    properties = fields.One2many(comodel_name="estate.property", inverse_name="type")
    offers = fields.One2many(related="properties.offers", inverse_name="property_type")

    offer_count = fields.Integer(compute="_compute_offer_count")

    _name_uniq = models.Constraint(
        'unique(name)',
        'A property type with the same name already exists.',
    )

    @api.depends("properties.offers")
    def _compute_offer_count(self):
        for type in self:
            type.offer_count = sum(len(property.offers) for property in type.properties)
