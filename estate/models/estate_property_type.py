from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Types of properties"
    _order = 'sequence, name asc'

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order types")
    offer_count = fields.Integer(compute="_compute_offer_count")

    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")

    _check_type_name = models.Constraint("UNIQUE(name)", "Type names must be unique.")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
