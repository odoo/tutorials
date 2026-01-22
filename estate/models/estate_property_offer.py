from odoo import fields, models


class EstateProperOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer."

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    # Because a One2many is a virtual relationship, there must be a Many2one field defined in the comodel.
    property_id = fields.Many2one('estate.property', required=True)
