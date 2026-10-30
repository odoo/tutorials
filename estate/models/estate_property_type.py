from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Contains the different types of properties"
    _check_name_is_unique = models.Constraint('UNIQUE(name)')
    _order = "sequence asc, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer()
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count")

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)


class EstatePropertyTypeProperty(models.Model):
    _name = "estate.property.type.property"
    _description = "Special view for properties by type"

    property_type_id = fields.Many2one("estate.property")
    name = fields.Char()
    expected_price = fields.Float()
    state = fields.Char()
