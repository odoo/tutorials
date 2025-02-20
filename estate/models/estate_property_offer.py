from datetime import date, timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Property Offers"
    _order = 'price desc'
    _check_company_auto = True
    _sql_constraints = [
        ('check_price', 'CHECK(price >0)', 'The Offer Price must be strickly Positive.')
    ]

    price = fields.Float(string="Offer Price", tracking=True)
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refuesd")
        ],
        tracking=True
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(
        string="Date Deadline",
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        store=True
    )

    property_type_id = fields.Many2one(
        'estate.property.type',
        string="Property Type",
        related='property_id.property_type_id'
    )

    # compute date deadline from today's date plus validity.
    @api.depends('create_date','validity')
    def _compute_date_deadline(self):
        for offer in self:
            if date.today():
                offer.date_deadline = date.today() + timedelta(days=offer.validity)
            else:
                offer.date_deadline = False

    # inverse method to compute validity from create date and deadline
    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days
            else:
                offer.validity = 7
                
    # action to check if any offer accepted then shows error
    # else change state to accepted and change selling price
    def action_accept(self):
        for offer in self:
            if offer.property_id.offer_ids.filtered(lambda x: x.status == 'accepted'):
                raise UserError("Only one offer can accepted.")
            offer.status = 'accepted'
            offer.property_id.write({
                'state': 'accepted',
                'selling_price': offer.price,
                'buyer_id': offer.partner_id,
            })
            offer.property_id.offer_ids.filtered(lambda x: x.id != offer.id).write({'status': 'refused'})

    # action to change offer status to refused
    def action_refuse(self):
        self.status = 'refused'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            offer_amount = vals.get('price')

            if property_id and offer_amount:
                property = self.env['estate.property'].browse(property_id)
                existing_offers = property.offer_ids.mapped('price')

                if existing_offers and offer_amount < max(existing_offers):
                    raise ValidationError(
                        "You cannot create an offer lower than an existing one."
                    )

                property.write({'state': 'received'})
        return super().create(vals_list)    

    # Individual cannot buy commercial properties.
    @api.constrains('partner_id', 'property_id')
    def _check_property_buyer(self):
        if any(
            offer.partner_id 
            and offer.property_id.property_type_id 
            and offer.property_id.property_type_id.id == offer.env.ref(
                'estate.property_type_commercial', raise_if_not_found=False).id
            and not offer.partner_id.is_company
            for offer in self
        ):
            raise UserError("Individuals cannot buy Commercial properties. "
                "Only companies are allowed.")

    # auto accept best offer using cron action
    def auto_accept_best_offer(self):
        today = date.today()

        properties = self.env['estate.property'].search([
            ('date_deadline', '&gt;=', today),
            ('state', '=', 'received')
        ])
        for property in properties:
            best_offer = property.offer_ids.filtered(lambda o: o.status != 'refused').sorted('price', reverse=True)[:1]

            if best_offer:
                best_offer.action_accept()
