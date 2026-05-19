from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name asc"

    estate_property_ids = fields.One2many(comodel_name="estate.property", inverse_name="estate_property_type_id")
    estate_property_offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_type_id")

    name = fields.Char(string="Type", required=True)
    sequence = fields.Integer(string='Sequence', default=1)
    offer_count = fields.Integer(compute="_compute_offer_count")

    _check_unique_name = models.UniqueIndex(definition="(UPPER(name))", message="Type should be unique")

    @api.depends('estate_property_offer_ids')
    def _compute_offer_count(self):
        for prop_type in self:
            prop_type.offer_count = len(prop_type.estate_property_offer_ids)
