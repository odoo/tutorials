from odoo import fields, models


class EstatePropertyType(models.Model):

    _name = 'estate.property.type'
    _description = "Estate Property Type"
    _order = 'sequence, name'

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "estate_property_type_id", string="Properties")
    partner_id = fields.Many2one('res.partner')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
