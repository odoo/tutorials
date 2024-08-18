from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate property type"
    name = fields.Char('Title', required = True)
    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="property_type_id")
    _order = "name"
    sequence = fields.Integer('Sequence', default = 1 )
    offer_ids = fields.One2many(comodel_name= "estate.property.offer", inverse_name= "property_type_id")
    offer_count = fields.Integer(compute="_compute_total_offers")
    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Type already exists!"),
    ]
    
    @api.depends('offer_ids')
    def _compute_total_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
        return