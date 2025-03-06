from odoo import api,fields,models # type: ignore


class estatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="Property Offer"

    price=fields.Float(string="Price")
    status=fields.Selection(
        selection=[
            ('accepted','Accepted'),
            ('refused','Refused')
        ])
    partner_id=fields.Many2one('res.partner',string="Partner",required=True, ondelete="cascade")
    property_id = fields.Many2one("estate.property", required=True, string="Property" )
    valadity = fields.Integer(string="Valadity(Days)",default="7")
    date_deadline = fields.Date(string="Deadline",compute="_compute_date_deadline",inverse="_inverse_date_deadline",store=True)
    