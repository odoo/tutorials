from odoo import fields, models


class InheritedEstateUser(models.Model):
    _name = ["estate.property.user"]
    _inherit = ["res.users"]

    property_ids = fields.One2many("estate.property" , inverse="user_id", domain="['|', ('state', '=', 'new' ),('state', '=', 'offer_received' )]")
