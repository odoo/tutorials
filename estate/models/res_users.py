from odoo import fields , models

class ReUsers(models.Model):
    _name = 'res.users'
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property','salesperson_id',string='Properties',domain=[("status","in",["new","offer received"])])
