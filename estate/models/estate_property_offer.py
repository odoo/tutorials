from odoo import fields,models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer model"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[
            ('accepted','Accepted'),
            ('refused','Refused'),
        ])
    partner_id = fields.Many2one("res.partner",required=True)
    property_id = fields.Many2one(comodel_name="estate.property",required=True)  
