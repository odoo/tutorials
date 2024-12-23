from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Types for real state properties"
    _order = "sequence, name"


    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property','property_type_id', string= 'Properties')
    sequence = fields.Integer('Sequence', default=1, help="Used to order types. Higher is more used.")
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer", inverse_name="property_type_id"
    )
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)


    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "Type Names MUST be unique."),
    ]
