from odoo import api,fields,models


class userInherited(models.Model):
    _inherit = ['res.users']

    property_ids = fields.One2many('estate.property','seller_id')
