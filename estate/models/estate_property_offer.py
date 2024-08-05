from odoo import models, fields


class EstatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "Estate property offer"

    price = fields.Float(string='Price', required=True)
    status = fields.Selection(string='Status',
                              selection=[
                                  ('accepted', 'Accepted'),
                                  ('refused', 'Refused')]
                              )
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Partner", copy=False)
    property_id = fields.Many2one(
        comodel_name="estate.property", string="Property")
