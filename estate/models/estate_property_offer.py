from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[('accepted', "Accepted"), ('rejected', "Rejected")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner ID", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
