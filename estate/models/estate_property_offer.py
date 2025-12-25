from dateutil.relativedelta import relativedelta

from odoo import _, api, exceptions, fields, models

class EstatePropertyOffer(models.Model):
    '''Offer for an estate property'''
    _name = "estate.property.offer"
    _description = "Offer for a property"
    _order = "price desc"

    # ==================== Fields ====================

    price = fields.Float("Price")
    status = fields.Selection(
        string = "Status",
        copy = False,
        selection = [('accepted', 'Accepted'), ('refused', 'Refused')]
    )
    partner_id = fields.Many2one("res.partner", required = True, string = "Partner")
    property_id = fields.Many2one("estate.property", required = True, string = "Property")
    date_deadline = fields.Date(compute = "_compute_date_deadline", inverse = "_inverse_date_deadline", string = "Deadline date")
    validity = fields.Float(default = 7, string = "Validity")
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    # ==================== Constaints  ====================

    _sql_constraints = [('check_price', 'CHECK(price > 0)', 'The price must be strictly positive.')]

    # ==================== Override Methods  ====================

    @api.model_create_multi
    def create(self, vals_list):
        '''Change property state and add price warning on creation'''

        for vals in vals_list:
            if 'property_id' in vals and 'price' in vals:
                property_id = self.env['estate.property'].browse(vals.get('property_id'))

                if property_id.offer_ids and vals.get('price') < min(property_id.offer_ids.mapped('price'), default=0):
                    raise exceptions.UserError(_("You are trying to create the lowest offer"))
                    
        
        offers = super().create(vals_list)
        offers.property_id.state = 'offer_received'

    # ==================== Compute Methods  ====================

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            start_date = offer.create_date or fields.Date.today()
            offer.date_deadline = start_date + relativedelta(days = offer.validity)

    @api.depends("date_deadline")
    def _inverse_date_deadline(self):
        for offer in self:
            start_date = offer.create_date or fields.Date.today()
            offer.validity = relativedelta(offer.date_deadline , start_date).days

    # ==================== Action Methods  ====================

    def action_accept_offer(self):
        '''Accept an offer'''
        self.ensure_one()

        if any(offer_id.status == 'accepted' for offer_id in self.property_id.offer_ids):
            raise exceptions.UserError(_("Another offer is already accepted"))
        
        self.status = 'accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        self.property_id.state = 'offer_accepted'

        return True

    def action_refuse_offer(self):
        '''Refuse an offer'''
        for offer in self:
            if offer.status == 'accepted':
                offer.property_id.buyer_id = False
                offer.property_id.selling_price = 0

            offer.status = 'refused'

        return True
