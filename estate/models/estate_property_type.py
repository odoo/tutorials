from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate_property_type'
    _unique_type = models.UniqueIndex("(name)",'property type should be unique')
    _order = "sequence"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1, help="Used to order the property types. Lower is better.")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(default=0,compute="_compute_total_count", store=True)
    property_ids = fields.One2many('estate.property','property_type_id')

    @api.depends('offer_ids')
    def _compute_total_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids.mapped('id'))
    
