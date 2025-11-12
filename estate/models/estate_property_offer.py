from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "An amount a potential buyer offers to the seller"
    _order = 'price desc'
    # constrain
    _sql_constraints = [
		('offer_price_positive', 'CHECK (price > 0.00)', "The offer price must be strictly positive.")
	]

    price = fields.Float(string="Price")
    validity = fields.Integer(string="Validity", default=7)
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused")
        ]
    )

    # relational fields
    partner_id = fields.Many2one(comodel_name='res.partner', required=True)
    property_id = fields.Many2one(comodel_name='estate.property', required=True)
    # related field
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    # computed field
    date_deadline = fields.Date(string="Deadline", compute='_compute_deadline', inverse='_inverse_deadline')

    # -------------------------------------------------------------------------
    # COMPUTE & INVERSE METHODS
    # -------------------------------------------------------------------------

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + relativedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today()  + relativedelta(days=offer.validity)

    def _inverse_deadline(self):
        """inverse function for validity to date of deadline calculation"""
        for offer in self:
            offer.validity = (offer.date_deadline - fields.Date.today()).days

    # -------------------------------------------------------------------------
    # CRUD OPERATIONS
    # -------------------------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        """offer creation criteria check & state change"""
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals['property_id'])
            if property.state == 'sold':
                raise UserError("The offer cannot create for sold proeprty.")

            max_price = property.best_price
            if vals['price'] <= max_price:
                raise UserError(f"The offer must be higher than {max_price}")
            elif property.state == 'new':
                    property.state = 'offer_received'

        return super().create(vals_list)

    @api.ondelete(at_uninstall=False)
    def _unlink_except_last_offer_set_property_state_new(self):
        """Ensure last offer deletion resets property state to 'new'."""
        property = self.property_id

        if property.state == 'sold':
            raise UserError("Cannot delete an offer for a sold property.")

        remaining_offers = property.offer_ids - self
        if not remaining_offers:
            property.state = 'new'

    # ------------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------------

    def action_accept(self):
        self.ensure_one()
        if self.property_id.state == 'sold':
            raise UserError("Property already sold.")
        elif self.property_id.state == 'cancelled':
            raise UserError("Property cancelled, offers cannot be accept.")
        elif self.status == 'accepted':
            raise UserError("Buyer is already accepted.")

        # except accepted one, other offers will be refused.
        for offer in self.property_id.offer_ids:
            if offer.id != self.id:
                offer.status = 'refused'
            else:
                self.write({'status': 'accepted'})
                self.property_id.write({
                    'selling_price': self.price,
                    'buyer_id': self.partner_id,
                    'state': 'offer_accepted'
                })

    def action_refuse(self):
        self.ensure_one()
        if self.property_id.state == 'sold':
            raise UserError("Property already sold.")
        elif self.property_id.state == 'cancelled':
            raise UserError("Property cancelled, offers cannot be refuse.")
        elif self.status == 'refused':
            raise UserError("Buyer is already refused.")

        self.status = 'refused'
