from odoo import api, exceptions, fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property.offer"
    _description = "Estate properties offers"

    price = fields.Float()
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy='false'
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    # -------------------------------------------------------------
    # computed field and their method
    # -------------------------------------------------------------
    validity = fields.Integer(string="Validity in days")
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if record.validity:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - fields.Date.today()).days
                   
    # -------------------------------------------------------------
    # UI actions
    # -------------------------------------------------------------
    def action_cancel(self):
        for record in self:
            record.status = 'refused'
        return True

    # When order is confirmed, update the status of all the offer and set the property selling_price and buyer
    def action_confirm(self):
        for record in self:
            if record.property_id.state == 'sold':
                raise exceptions.UserError('Property already sold')
            current_offer_id = record.id
            for offer in record.property_id.offer_ids:
                if offer.id == current_offer_id:
                    offer.status = 'accepted'
                    offer.property_id.selling_price = offer.price
                    offer.property_id.buyer_id = offer.buyer_id
                else:
                    offer.status = 'refused'
        return True
        