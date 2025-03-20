from odoo import fields, models, api


class EstatePropertyTypesModel(models.Model):
    _name = "estate.property.types"
    _description = "The estate property types model"
    _order = "name asc"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", "")
    sequence = fields.Integer(default=1, help="used for manual ordering")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ("check_property_type", "UNIQUE(name)", "The property type must be unique")
    ]
