from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for the properties of the estate module"
    _order = "id desc"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        help='Current status of the offer (Accepted or Refused).'
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            start = (record.create_date or fields.Datetime.now()).date()
            record.date_deadline = fields.Date.add(start, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start = (record.create_date or fields.Datetime.now()).date()
            record.validity = (record.date_deadline - start).days

    def action_accept_offer(self):
        for record in self:
            if record.status == 'refused':
                raise UserError(self.env._("You cannot accept a refused offer."))
            if record.property_id.state in ("offer_accepted", "sold", "cancelled"):
                raise UserError(self.env._("An offer has already been accepted or the property is not availabe."))
            record.status = 'accepted'
            record.property_id.state = 'offer_accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    def action_refuse_offer(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError(self.env._("You cannot refuse an accepted offer."))
            record.status = 'refused'
        return True

    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'An offer price must be strictly positive'
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            estate_property = self.env["estate.property"].browse(vals["property_id"])
            if estate_property.state == 'sold':
                raise UserError(self.env._("You cannot create an offer for a sold property."))
            if float_compare(vals["price"], estate_property.best_price, precision_digits=2) != 1:
                raise UserError(self.env._("The offer must be higher than the existing offers."))
            estate_property.state = 'offer_received'
        return super().create(vals_list)
