from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offerf"

    partner_id = fields.Many2one('res.partner', string='buyer')
    status = fields.Selection(
        string='status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False
    )
    price = fields.Char(required=True)
    property_id = fields.Many2one(
        comodel_name="estate.property",
        string="property"
    )
