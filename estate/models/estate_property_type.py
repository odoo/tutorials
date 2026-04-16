from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property_type"
    _description = "Defines property type"
    _order = "sequence,name"

    name = fields.Char(string="Property Type", required=True)
    property_ids = fields.One2many("estate_property", "property_type_id")
    sequence = fields.Integer(string="Sequence", default=1)
    offer_ids = fields.One2many(
        comodel_name="estate.property_offer", inverse_name="property_type_id"
    )
    offer_count = fields.Integer(compute="_compute_offer_count")

    _name_unique = models.UniqueIndex("(name)", "name must be unique")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
