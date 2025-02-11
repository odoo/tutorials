from odoo import models,fields

class ResUser(models.Model):
    _inherit="res.users"

    property_res_ids=fields.One2many('estate.property',
        'property_seller_id',
        string='Properties',
        domain="[('status', 'in', ['new', 'offer_received'])]"
    )

