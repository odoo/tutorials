from odoo import api, fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of real estate properties"
    _order = "sequence, name"

    name = fields.Char('Title', required=True)
    property_ids = fields.One2many('estate.property','property_type_id','Properties')
    offer_ids = fields.One2many('estate.property.offer','property_type_id', string="Offer")
    offer_count = fields.Integer('Number of offers', compute="_compute_total_offers")
    sequence = fields.Integer('Sequence', help="Used to order type property.")

    _sql_constraints = [
        ('unique_name','UNIQUE(name)','The Type must be UNIQUE.')
    ]    

    @api.depends('offer_ids')
    def _compute_total_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
    
    def action_view_offers(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Offers',
            'res_model': 'estate.property.offer',
            'view_mode': 'list,form',
            'domain': [('property_type_id', '=', self.id)],
            'context': {'default_property_type_id': self.id},
        }