from odoo import fields, models


class ResUsers(models.Model):
    _inherit = ['res.users']

    property_ids = fields.One2many(
        'ninja.turtles.estate',
        'salesperson_id',
        string="Properties",
        domain=[('status', '!=', 'sold')],
    )

    offer_ids = fields.One2many(
        "ninja.turtles.estate.property.offer",
        "property_type_id",
        string="Offers",
    )
