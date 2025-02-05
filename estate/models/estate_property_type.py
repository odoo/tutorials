from odoo import fields, models , api

class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Test Property"

    name = fields.Char(required=True) 
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    ) 
    _sql_constraints = [
        ('unique_type_name', 
         'UNIQUE(name)', 
         'The property type name must be unique!')
    ] 
    sequence = fields.Integer(string='Sequence', default=10)
    _order = "sequence,name"
    offer_count = fields.Integer(
        string="Offer Count",
        compute="_compute_offer_count",
        store=True,
    ) 
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_type_id",
        string="Offers",
    ) 

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
            
    def action_view_offers(self):
        return {
        'type': 'ir.actions.act_window',
        'name': 'Offers',
        'res_model': 'estate.property.offer',
        'view_mode': 'list,form', 
        'domain': [('property_id.property_type_id', '=', self.id)],
        'context': {'default_property_id': self.property_ids.ids},
    }
        