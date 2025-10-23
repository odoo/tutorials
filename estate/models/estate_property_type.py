from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"
    _name_unique = models.Constraint("unique (name)", "Ce type de propriété existe déjà.")

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_count")

    @api.depends("offer_ids")
    def _compute_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
