from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="Real Estate Property Type"
    _order = "Sequence" 

    name=fields.Char(string="Name" , required=True)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(string="Offer Count", store=True, compute="_compute_offer_count")
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    Sequence = fields.Integer('Sequence', default=10)

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
            
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'Property type names must be unique.')]
