from odoo import api, fields, models, exceptions
from dateutil.relativedelta import relativedelta
import datetime


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"
    _order = "price desc"

    _check_price = models.Constraint('CHECK(price > 0)', 'The price should always be positive')

    price = fields.Float()
    status = fields.Selection(readonly=True, selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_validity", readonly=False)
    property_type_id = fields.Many2one(related="property_id.property_type_id")


    @api.model
    def create(self, vals_list):
        prop = self.env['estate.property'].browse(vals_list[0]['property_id'])

        if(any(o.price > vals_list[0]['price'] for o in prop.offer_ids)):
            raise exceptions.UserError("Cannot add an offer with a lower amount than an existing one")

        prop.state = "offer-received"

        return super().create(vals_list)


    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for r in self:
            create = r.create_date.date() if isinstance(r.create_date, datetime.datetime) else fields.Date.today() 
            r.date_deadline = create + relativedelta(days=r.validity)

    
    def _inverse_validity(self):
        for r in self:
            create = r.create_date.date() if isinstance(r.create_date, datetime.datetime) else fields.Date.today()
            r.validity = (r.date_deadline - create).days


    def accept_offer(self):
        for r in self:
            if(r.status == 'accepted'):
                continue

            for other in r.property_id.offer_ids:
                if(other.status == 'accepted'):
                    raise exceptions.UserError("Cannot accept multiple offers for a single property")

            r.status = 'accepted'
            r.property_id.buyer_id = r.partner_id
            r.property_id.selling_price = r.price
            r.property_id.state = "offer-accepted"
        return True


    def refuse_offer(self):
        for r in self:
            if(r.status == 'accepted'):
                r.property_id.buyer_id = None
                r.property_id.selling_price = None
            r.status = 'refused'
        return True
