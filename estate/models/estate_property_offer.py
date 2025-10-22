from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "property offer"

    price = fields.Float('price')
    status = fields.Selection(
        string='status',
        selection=[('Accepted', 'Accepted'), ('Refused', 'Refused')],
        copy=False)
    partner_id = fields.Many2one("res.partner", string="partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
