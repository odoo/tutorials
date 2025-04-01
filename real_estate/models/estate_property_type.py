from odoo import models, fields,api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "name desc"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'A property type name must be unique')
    ]
 
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids.mapped(id))
