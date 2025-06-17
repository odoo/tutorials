from odoo import models, fields, api


class PropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Possible types of the properties in the Estate app"

    _sql_constraints = [('unique_type_name', 'UNIQUE(name)', 'The Type names should be unique')]
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer("Sequence", default=1, help="Used to order types in views, lower is better.")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count_by_type")

    @api.depends("offer_ids")
    def _compute_offer_count_by_type(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
