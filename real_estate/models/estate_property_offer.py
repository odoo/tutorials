from datetime import date, timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    # Offers for the property

    _name = "estate.property.offer"
    _description = "Property Offers"
    _order = "price desc"

    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "offer price must be positive")
    ]

    price = fields.Float(
        string="Offer Price",
        help="Price for the offer"
    )
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        help="Current status of the property",
        copy=False,
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True,
        help="Partner assigned for the sale"
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
        help="Property for sale"
    )
    validity = fields.Integer(
        string="Validity",
        default=7,
        help="Validity period of the offer"
    )
    date_deadline = fields.Date(
        string="Date Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )
    create_date = fields.Date(
        string="Create Date",
        default=fields.Date.context_today
    )
    property_type_id = fields.Many2one(
        'estate.property.type',
        string="Type",
        related='property_id.property_type_id'
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        # Compute deadline date based on create_date and validity period.
        for offer in self:
            offer.date_deadline = (
                offer.create_date + timedelta(days=offer.validity)
                if offer.create_date else False
            )

    def _inverse_date_deadline(self):
        # Inverse function to calculate validity from date_deadline.
        for offer in self:
            offer.validity = (
                (offer.date_deadline - offer.create_date).days
                if offer.date_deadline else 7
            )
    
    def action_confirm(self):
        for offer in self:
            # Check if the property is already sold
            if offer.property_id.state == 'sold':
                raise UserError("Property is already sold")
            
            if offer.property_id.offer_ids.filtered(lambda x: x.status == 'accepted'):
                raise UserError("Only one offer can be accepted")

            # Update the offer status using CRUD method
            offer.write({'status': 'accepted'})
            offer.property_id.write({
                'buyer_id': offer.partner_id.id,
                'selling_price': offer.price
            })
    
    def action_refused(self):
        for property in self:
            if property.status == 'accepted':
                property.property_id.buyer_id = False
                property.property_id.selling_price = 0.0
            property.status = 'refused'

    @api.model_create_multi
    def create(self,vals):
        for val in vals:
            if (property_id := val.get('property_id')) and (offer_amount := val.get('price')):
                property = self.env['estate.property'].browse(property_id)
                existing_offer = property.offer_ids.mapped('price')
                if existing_offer and offer_amount < max(existing_offer):
                    raise ValidationError("Cannot create offer less than current offer")
                property.write({'state': 'offer_received'})
        return super().create(vals)

    @api.model
    def _cron_auto_confirm_best_offer(self):
        today = date.today()
        
        # Find properties that have offers and have exceeded their deadline
        expired_properties = self.env['estate.property'].search([
            ('date_deadline', '<=', today),
            ('state', '=', 'offer_received')
        ])

        for property in expired_properties:
            best_offer = property.offer_ids.filtered(lambda o: o.status != 'refused').sorted('price', reverse=True)[:1]

            if best_offer:
                best_offer.action_confirm()
