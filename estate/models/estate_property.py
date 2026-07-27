from odoo import fields, models, api, exceptions
from odoo.tools import float_utils
from datetime import timedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Module"
    _order = "id desc"


    _check_positif_expected_price = models.Constraint(
        'CHECK(expected_price >= 0)',
        'The expected price must be positive'
    )
    _check_positif_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price must be positive'
    )

    # Base Fields

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", copy=False, readonly=True)
    best_price = fields.Integer(string="Best Price", compute="_compute_best_price")
    expected_date = fields.Date(
        string="Expected Date",
        required=True,
        copy=False,
        default=(fields.Date.today() + timedelta(days=90)),
    )
    bedroom = fields.Integer(string="Number of Bedroom", default=2)
    living_area = fields.Integer(string="Living area (square metter)")
    facades = fields.Integer(string="Number of facades")
    garage = fields.Boolean(string="Have a garage?")
    garden = fields.Boolean(string="Have a garden?")
    garden_area = fields.Integer(string="Garden area (square metter)")
    garden_orientation = fields.Selection(
        string="Garden's orientation",
        selection=[
            ("north", "North"),
            ("sud", "Sud"),
            ("east", " East"),
            ("west", "West"),
        ],
    )
    total_area = fields.Integer(string="Total Area", compute="_compute_total_area")
    state = fields.Selection(
        string="Estate's state",
        selection=[
            ("new", "New"),
            ("offer_recieved", "Offer Received"),
            ("offer_accepted", " Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )
    salesman_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tag")
    proterty_offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    active = fields.Boolean(default=True)



    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('proterty_offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.proterty_offer_ids.mapped('price')
            record.best_price = max(prices, default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''
        # return {'warning': {'title': "Test warning", 'message': "foo", 'type': 'notification'},}

    @api.constrains("selling_price", "expected_price")
    def _check_price_expectation(self):
        for record in self:
            if float_utils.float_is_zero(record.selling_price, 0):
                return True
            if float_utils.float_compare(record.selling_price, record.expected_price * 0.9, 2) == -1:
                raise exceptions.ValidationError("Selling price can't be smaller than 90% of the expected price")
        return True

    @api.ondelete(at_uninstall=False)
    def delete(self):
        for record in self:
            if record.state not in ["new", "cancelled"]:
                raise exceptions.UserError(f"Can't delete an advertise in {record.state} state")


    def action_sold_adv(self):
        for advertisements in self:
            if advertisements.state == "cancelled":
                raise exceptions.UserError("Can't sold an canceled advertise")
            advertisements.state = "sold"
        return True

    def action_cancel_adv(self):
        for advertisements in self:
            if advertisements.state == "sold":
                raise exceptions.UserError("Can't cancel an sold advertise")
            advertisements.state = "cancelled"
        return True

    def accept_offer(self):
        for adrivertise in self:
            # offer = [offer for offer in adrivertise.proterty_offer_ids if offer.status == 'accepted' ][0]
            accepted_offer = list()
            for offer in adrivertise.proterty_offer_ids:
                if accepted_offer:
                    offer.status = "refused"
                elif offer.status == 'accepted':
                    accepted_offer.append(offer)
                else:
                    offer.status = 'refused'

            accepted_offer = accepted_offer[0]
            adrivertise.buyer_id = accepted_offer.partner_id
            adrivertise.selling_price = accepted_offer.price
            adrivertise.state = 'offer_accepted'

    def set_offer_received(self):
        for record in self:
            record.state = "offer_recieved"
