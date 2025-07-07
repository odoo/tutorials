from odoo import  api,fields,models
from datetime import timedelta
from odoo.exceptions import UserError,ValidationError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property OFFER created"

    price=fields.Float()
    status = fields.Selection(
        selection=[('accepted','Accepted'), ('refused','Refused')],
        copy=False,
    )

    partner_id = fields.Many2one("res.partner",string="Partner",index=True,required=True,default=lambda self:self.env.user.partner_id.id)
    property_id = fields.Many2one("estate.property",index=True,required=True)

    validity = fields.Integer(default = 7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )

    _sql_constraints = [
        ('offer_price_positive','CHECK(price>=0)','The offer price should be positive.')
    ]

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                create_date = record.create_date.date()
            else:
                create_date = fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)


    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                create_date = record.create_date.date()
            else:
                create_date = fields.Date.today()
            if record.date_deadline:
                record.validity = (record.date_deadline - create_date).days


    
    def accept_icon_action(self):
        for record in self:
            # Ensure only one accepted offer per property
            if any(
                offer.status == 'accepted'
                for offer in record.property_id.offer_ids
            ):
                raise UserError("Only one offer can be accepted per property.")

            # ✅ Enforce 90% price check
            min_price = record.property_id.expected_price * 0.9
            if float_compare(record.price, min_price, precision_digits=2) < 0:
                raise ValidationError("Offer must be at least 90% of the expected price to be accepted.")
        
            record.status = 'accepted'

            # Refuse all other offers
            other_offers = record.property_id.offer_ids - record
            other_offers.write({'status': 'refused'})

            # Set buyer and selling price on property
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id

    def refuse_icon_action(self):
        for record in self:
            record.status = 'refused'
