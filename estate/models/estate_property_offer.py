from odoo import fields, models, api
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "this is property offer model"
    _order = "price desc"

    price = fields.Float('Price')
    status = fields.Selection(
        [('accepted', "Accepted"), ('refused', "Refused")], copy=False
    )
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date(
        "date_deadline", compute="_compute_date_deadline", inverse="inverse_date_deadline"
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', readonly=True)
    property_type_id = fields.Many2one(
    "estate.property.type",
    related="property_id.property_type_id",
    store=True,
    string="Property Type"
    )

    _check_offer_price = models.Constraint(
        'CHECK( price > 0)', "The offer price must be Strictly positive"
    )
   
    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                record.create_date or fields.Date.today(), days=record.validity
            )

    def inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_confirm(self):
        for record in self:
            if record.property_id.state == 'offer_accepted':
                raise UserError(message="You can't Accept multiple offer")
            else:
                record.status = 'accepted'
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
                record.property_id.state = 'offer_accepted'
                for offer in record.property_id.offer_ids:
                    if record.id != offer.id:
                        offer.status='refused'
        return True

    def action_cancel(self):
        for record in self:
            record.status = 'refused'
        return True
