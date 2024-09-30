from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property.type"
    _description = "EstatePropertyType"
    _order = "name"
    name = fields.Char("Property Types", required=True)
    _sql_constraints = [
        ("uniq_propertytype", "unique(name)", "A property type name must be unique"),
    ]
    property_ids = fields.One2many("estate.property", "property_type")
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer", inverse_name="property_type_id"
    )
    offer_count = fields.Integer(compute="_num_of_offers", string="Offer Count")
    sequence = fields.Integer(
        "Sequence", default=1, help="To manually reorder property types"
    )

    api.depends("offer_id")

    def _num_of_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
