from odoo import models, fields # type: ignore

class TestEstatePropertyOffer(models.Model):
    _name = "test.estate.property.offer"
    _description = "This is test offer Table."
    
    test_price = fields.Float(required=True)
    test_status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
        help="status of offer"
    )
    test_partner_id = fields.Many2one(
        'res.partner',
        required=True
    )
    test_property_id = fields.Many2one(
        'estate.property',
        required=True
    )

    
