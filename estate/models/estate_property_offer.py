from odoo import api, models, fields
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float("Offer Price", required=True)
    status = fields.Selection(selection=[
        ('accepted', 'ACCEPTED'),
        ('refused', 'REFUSED')
        ])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer('Validity', default=7)
    date_deadline = fields.Date('Date Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", string="Property Type", store=True
    )
    _order = 'price desc'

    _sql_constraints = [
        ('price', 'CHECK(price > 0)',
        'The price of an offer should be strictly grater than 0.')
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val.get("property_id") and val.get("price"):
                prop = self.env["estate.property"].browse(val["property_id"])

                if prop.offer_ids:
                    max_offer = max(prop.mapped("offer_ids.price"))
                    if float_compare(val["price"], max_offer, precision_rounding=0.01) <= 0:
                        raise UserError("The offer must be higher than %.2f" % max_offer)
                prop.state = "offer_received"
        return super().create(vals_list)

    def action_accept(self):
        for offer in self.property_id.offer_ids:
            if offer.status == 'accepted':
                raise UserError("An offer has already been accepted for this property.")
        if self.status != 'accepted':
            if self.property_id.state == 'sold':
                raise UserError("You can't accept an offer for a property already sold")
            self.status = 'accepted'
            self.property_id.state = 'offer_accepted'
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id.id
        else:
            raise UserError("You can't accept an offer already accepted")

    def action_refuse(self):
        if not self.status:
            self.status = 'refused'
        else:
            raise UserError("You can't refuse an offer already refused or already accepted")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.context_today(record)
            record.date_deadline = create_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = 0
