from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name "

    sequence = fields.Integer(default=1)
    name = fields.Char(required = True)
    property_ids = fields.One2many("estate.property","property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer","property_type_id")
    offer_count= fields.Integer(string="Offer Count", compute="_compute_offer_count")
    sql_constraints = [
        ("unique_type_name", "UNIQUE(name)", "The property type name must be unique."),
    ]

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
