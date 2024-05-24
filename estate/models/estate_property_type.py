from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Estate property Type"
    _order = "sequence,name"
    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)

    _sql_constraints = [
        ('check_unique', 'UNIQUE(name)',
         'Value must be unique.')
    ]
    property_ids = fields.One2many("estate_property", "property_type_id")
    offer_ids = fields.One2many("offer", "property_type_id")
    offer_count = fields.Float(compute="_compute_total")

    @api.depends("offer_ids")
    def _compute_total(self):
        self.offer_count = len(self.offer_ids)
