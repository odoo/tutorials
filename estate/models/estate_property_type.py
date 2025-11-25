from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "property types"
    _order = "sequence, name asc"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1)

    property_ids = fields.One2many(
        comodel_name="estate.property", inverse_name="property_type_id"
    )
    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count", default=0, string="Offers")

    _unique_type = models.Constraint("unique(name)", "This type already exists")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for type in self:
            type.offer_count = len(type.offer_ids)
