from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types"
    _order = "sequence, name"

    _sql_constraints = [
        ('unique_prop_type', 'UNIQUE(name)', 'This property type already exists.')
    ]

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many(
        comodel_name="estate.property", inverse_name="property_type_id")
    sequence = fields.Integer(default=1)
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer", inverse_name="property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
