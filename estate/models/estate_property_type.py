from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "type of estate property"
    _sql_constrains = [
        ('check_name', 'UNIQUE(name)',
         'Type name has to be unique')
    ]
    _order = "name asc"

    name = fields.Char(required=True, string="Name")
    property_ids = fields.One2many("estate.property", "property_type_id", string="property id")
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="offer ids")
    offer_count = fields.Integer(compute="_compute_offer_count")

    # -------------------- COMPUTE FUN 
    
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)