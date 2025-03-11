from odoo import fields, models, api

class estate_Property_Type(models.Model):
    _name = "estate.property.type"
    _description = "relevent type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property","property_ids", string="Properties")
    sequence = fields.Integer("Sequence", default=10)
    offer_ids = fields.One2many("estate.property.offer","property_type_id", string="Offers")
    offer_count = fields.Integer(compute = "_compute_offer_count", default = 0)

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids.mapped(id))
   
    _sql_constraints = [
        ('check_type_name', 'UNIQUE(name)','The name must be unique.')
    ]
