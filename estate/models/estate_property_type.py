from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types"
    _order = "sequence, name desc"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order properties. Lower is better.")
    offer_count = fields.Integer(compute="_compute_offer_count")

    property_ids = fields.One2many("estate.property","property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer","property_type_id", string="Offers")

    _sql_constraints = [
        ('unique_name_types','UNIQUE(name)','Property Types should be unique')
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
