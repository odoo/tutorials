from odoo import models,fields,api

class estate_property(models.Model):
    _name = 'estate.property'
    _description = "This property is for sell"

    def _default_name(self):
        return self.get_value()
    
    name = fields.Char(string='Name',_default = lambda self:self._default_name(),required=True, tracking=True)
    description = fields.Text(string='Description', tracking=True)
    postcode = fields.Char(String='postcode')
    garden = fields.Boolean(string='Garden')
    garden_orientation = fields.Selection(string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ])
    
