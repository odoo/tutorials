from odoo import api, fields, models, exceptions
from dateutil.relativedelta import relativedelta
from datetime import date

class PropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "Estate property offers"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')]
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    sql_constraints = [
        ('check_positive_price', 'CHECK(price > 0)',
         'A property offer price must be strictly positive.')
    ]

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + relativedelta(days=offer.validity)
            else:
                offer.date_deadline = date.today() + relativedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer.create_date.date()).days

    def action_accept(self):
        # To get the statuses of all offers related to the property
        # print(self.mapped("property_id.offer_ids.status"))
        related_offers = self.mapped("property_id.offer_ids.status")
        if any([x == 'accepted' or False for x in related_offers]):
            raise exceptions.UserError("Another offer was already accepted")
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.state = 'offer_accepted'
        self.property_id.buyer_id = self.partner_id
        return True

    def action_refuse(self):
        self.status = 'refused'
        return True

