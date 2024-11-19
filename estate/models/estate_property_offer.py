from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = ''

    price = fields.Float()
    status = fields.Selection([
        ('accepted','Accepted'),
        ('refused','Refused'),
    ],
        copy=False,
    )

    # Relations
    partner_id = fields.Many2one(comodel_name='res.partner', requird=True)
    property_id = fields.Many2one(comodel_name='estate.property', requird=True)

