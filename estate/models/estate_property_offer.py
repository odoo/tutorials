from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers related to property are made"

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refuse')],
        copy = False,
    )
    partner_id = fields.Many2one(
        "res.partner",string='Partner',index = True,  default = lambda self: self.env.user.partner_id.id
)
    property_id = fields.Many2one("estate.property",index = True, required = True)
    validity = fields.Integer(default = 7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The offer price must be greater than 0')
    ]

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            # Use create_date if available, otherwise fallback to today
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            if record.date_deadline:
                record.validity = (record.date_deadline.day - create_date.day)
                
    def action_confirm(self):
        for offer in self:
            # Check if already accepted offer exists for the property
            existing_offer = offer.property_id.offer_ids.filtered(lambda o: o.status == 'accepted' and o.id != offer.id)
            if existing_offer:
                raise UserError("Only one offer can be accepted per property.")

            # Set accepted
            offer.status = 'accepted'
            # Set buyer and selling price on the property
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = 'offer accepted'
            


    def action_refuse(self):
        for record in self:
            record.status = 'refused'


    
 