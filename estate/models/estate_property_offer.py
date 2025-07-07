from odoo import fields, models, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers of Estate property "

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection = [
            ('accepted','Accepted'),
            ('refused','Refused')
        ], copy=False,string='Status'
    )

    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline_date", inverse="_inverse_deadline_date")

    partner_id = fields.Many2one("res.partner", string="Partner",copy=False,required=True)
    property_id = fields.Many2one("estate.property",copy=False,required=True)



    @api.depends('create_date','validity')
    def _compute_deadline_date(self):
        for offer in self:
            create_dt = offer.create_date or fields.Date.today()
            offer.date_deadline = create_dt + relativedelta(days=offer.validity)


    def _inverse_deadline_date(self):
        for offer in self:
            if offer.date_deadline:
                create_dt = (offer.create_date or fields.Datetime.now()).date()
                delta = (offer.date_deadline - create_dt).days
                offer.validity = delta
            else:
                offer.validity = 0

    def action_accept(self):
        for offer in self:
            # Allow only if property has no accepted offer
            if offer.property_id.buyer_id:
                raise UserError(_("An offer has already been accepted for this property."))
            # Set buyer and selling price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.status = 'accepted'
            # Setting remaining Offer as refused
            other_offers = offer.property_id.offer_id - offer
            # for other in other_offers:                  # -----> Normal for loop logic
            #     other.status = 'refused'
            other_offers.write({'status': 'refused'})     # -----> Odoo ORM Method

        return True

    def action_refused(self):
        for offer in self:
            offer.status = 'refused'
        return True
