from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import date_utils


class RealEstateOffer(models.Model):
    _name = 'real.estate.offer'
    _description = "Real Estate Offer"
    _sql_constraints = [
        ('positive_amount', 'CHECK (amount > 0)', "The amount must be strictly positive.")
    ]

    amount = fields.Float(string="Amount", required=True)
    buyer_id = fields.Many2one(string="Buyer", comodel_name='res.partner', required=True)
    phone = fields.Char(string="Phone", related='buyer_id.phone')
    date = fields.Date(string="Date", required=True, default=fields.Date.today)
    validity = fields.Integer(
        string="Validity", help="The number of days before the offer expires.", default=7
    )
    expiry_date = fields.Date(
        string="Expiry Date",
        compute='_compute_expiry_date',
        inverse='_inverse_expiry_date',
        store=True,
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

    @api.constrains('amount')
    def _check_amount_higher_than_previous_offers(self):
        for offer in self:
            same_buyer_offers = offer.property_id.offer_ids.filtered(
                lambda o: o.buyer_id == offer.buyer_id
            )
            if offer.amount < max(same_buyer_offers.mapped('amount')):
                raise ValidationError(_(
                    "The amount of the new offer must be higher than the amount of the previous "
                    "offers."
                ))

    @api.constrains('state')
    def _check_state_is_accepted_for_only_one_offer(self):
        for offer in self.filtered(lambda o: o.state == 'accepted'):
            if len(offer.property_id.offer_ids.filtered(lambda o: o.state == 'accepted')) > 1:
                raise ValidationError(_("Only one offer can be accepted for a property."))

    @api.model_create_multi
    def create(self, vals_list):
        offers = super().create(vals_list)
        for offer in offers:
            if offer.property_id.state == 'new':
                offer.property_id.state = 'offer_received'
        return offers

    def unlink(self):
        for offer in self:
            property_offers = offer.property_id.offer_ids
            if (
                offer.property_id.state in ('offer_received', 'under_option')
                and not (property_offers - self)  # All the property's offers are being deleted.
            ):
                offer.property_id.state = 'new'
        return super().unlink()

    def action_accept(self):
        self.state = 'accepted'
        self.property_id.state = 'under_option'
        (self.property_id.offer_ids - self).state = 'refused'
        return True

    def action_refuse(self):
        self.state = 'refused'
        return True

    @api.model
    def _refuse_expired_offers(self):
        expired_offers = self.search([('expiry_date', '<', fields.Date.today())])
        expired_offers.action_refuse()
