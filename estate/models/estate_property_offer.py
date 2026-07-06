from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "this model is for estate property offers"

    price = fields.Float()
    status = fields.Selection(
        [('accepted', "Accepted"), ('refused', "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True, ondelete="cascade")
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Date.today()
            offer.date_deadline = create_date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = offer.create_date.date() or fields.Date.today()
            if offer.date_deadline and create_date:
                offer.validity = (offer.date_deadline - create_date).days

    def action_accept(self):
        for offer in self:
            existing_accepted = offer.property_id.offer_ids.filtered(
                lambda o: o.status == 'accepted'
            )
            if existing_accepted:
                raise UserError(
                    message="An offer has already been accepted for this property!"
                )
            offer.status = "accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer = offer.partner_id
            offer.property_id.state = 'offer_accepted'
        return True

    def action_refuse(self):
        for offer in self:
            if offer.status == "accepted":
                offer.status = "refused"
                # message = "nothing but smilely"
                # return {
                #     'effect': {
                #         'fadeout': 'slow',
                #         'message': message,
                #         'img_url': '/web/static/src/img/smile.svg',
                #         'type': 'rainbow_man',
                #     }
                # }

                # return {
                #     'type': 'ir.actions.client',
                #     'tag': 'display_notification',
                #     'params': {
                #         'title': 'Offer Refused',
                #         'message': 'The offer has been successfully refused.',
                #         'type': 'warning',
                #         'sticky': False,
                #     },
                # }
        return True

    def action_make_validity_default(self):
        for offer in self:
            offer.validity = 7
        return True
