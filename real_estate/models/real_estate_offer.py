from odoo import api, fields, models
from odoo.tools import date_utils


class RealEstateOffer(models.Model):
    _name = 'real.estate.offer'
    _description = "Real Estate Offer"

    amount = fields.Float(string="Amount", required=True)
    buyer_id = fields.Many2one(string="Buyer", comodel_name='res.partner', required=True)
    date = fields.Date(string="Date", required=True, default=fields.Date.today)
    validity = fields.Integer(
        string="Validity", help="The number of days before the offer expires.", default=7
    )
    expiry_date = fields.Date(
        string="Expiry Date", compute='_compute_expiry_date', inverse='_inverse_expiry_date'
    )
    state = fields.Selection(
        string="State",
        selection=[
            ('waiting', "Waiting"),
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        required=True,
        default='waiting',
    )
    property_id = fields.Many2one(
        string="Property", comodel_name='real.estate.property', required=True
    )

    @api.depends('date', 'validity')
    def _compute_expiry_date(self):
        for offer in self:
            offer.expiry_date = date_utils.add(offer.date, days=offer.validity)

    def _inverse_expiry_date(self):
        for offer in self:
            offer.validity = date_utils.relativedelta(dt1=offer.expiry_date, dt2=offer.date).days
