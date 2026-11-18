from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property"
    _order = "name"
    _check_unique = models.UniqueIndex("(name)", "All property types need to have a unique name")

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1, help="Used to order types. Lower values come first.")
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers for this type")
    offer_count = fields.Integer(compute="_count_nb_offers")

    @api.depends("offer_ids")
    def _count_nb_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
