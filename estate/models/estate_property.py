import datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError

from .. import fields as estate_fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    _sql_constraints = [
        ('estate_property_check_bedrooms', 'CHECK(bedrooms IS NULL OR bedrooms >= 0)',
         'Bedrooms must be a non-negative number or NULL.'),
        ('check_facades', 'check(facades is NULL OR (facades >= 0 AND facades <= 4))',
         'The number of facades must be 0 <= facades <= 4'),
        ('expected_price_strictly_positive', 'CHECK(expected_price > 0)',
         'The expected price must be strictly positive'),
        ('name_uniq', 'unique (name)', 'Estate property already exists!')
    ]

    name = fields.Char("Name", required=True, index=True, help="Name of the property", copy=False)
    description = fields.Text("Description", translate=True)
    postcode = fields.Char("Postcode", help="Postcode of the property")
    available_from = fields.Date("Date", required=True,
                                 default=lambda _: datetime.date.today() + datetime.timedelta(days=30 * 3))
    postgis_location = estate_fields.PointField("Location", required=False)
    expected_price = fields.Float(
        required=True,
        help="The price you expect the property to be sold for",
    )
    minimum_sale_price = fields.Float("Minimum sale price", compute="_compute_minimum_sale_price")
    selling_price = fields.Float("Selling price", compute="_compute_selling_price")
    bedrooms = fields.Integer("Bedrooms", default=2, required=False, help="Number of bedrooms of your property")
    living_area = fields.Float("Living area (sqm)", default=0)
    facades = fields.Integer("Facades", required=False, help="Number of facades of your property")
    garage = fields.Boolean("Garage", default=False)
    garden = fields.Boolean("Has a garden", required=True, default=False, help="Whether the property has a garden")
    garden_area = fields.Float("Garden area (sqm)", default=lambda self: self._garden_area_default())
    garden_orientation = fields.Selection(
        string="Garden orientation",
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        default=lambda self: self._garden_orientation_default()
    )
    state = fields.Selection(
        string="State",
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        default="new",
        required=True,
        copy=False,
        readonly=False,
        help="State of the property.\n"
             "new: A new property that has just been listed.\n"
             "offer_received: An offer has been made on the property.\n"
             "offer_accepted: The seller has accepted an offer.\n"
             "sold: The property has been sold and the sale is finalized.\n"
             "canceled: The listing has been canceled.",
    )
    active = fields.Boolean('Active', default=True)
    property_type_id = fields.Many2one("estate.property.type", "Property types")
    buyer_id = fields.Many2one("res.partner", "Buyer", compute="_compute_buyer")
    salesperson_id = fields.Many2one("res.users", "Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float("Total area", compute="_compute_total_area", store=True)
    best_offer = fields.Float("Best offer", compute="_compute_best_offer", store=True)

    def _garden_area_default(self):
        return 10

    def _garden_orientation_default(self):
        return 'north'

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area = self.garden and self._garden_area_default() or None
        self.garden_orientation = self.garden and self._garden_orientation_default() or None

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'), default=0)

    @api.depends("offer_ids.price")
    def _compute_selling_price(self):
        for record in self:
            record.selling_price = next(
                (offer.price for offer in record.mapped("offer_ids") if offer.status == 'accepted'), 0)

    @api.onchange("offer_ids")
    def _onchange_offer_ids(self):
        self.update_state()

    @api.depends("offer_ids.partner_id")
    def _compute_buyer(self):
        for record in self:
            record.buyer_id = next(
                (offer.partner_id for offer in record.mapped("offer_ids") if offer.status == 'accepted'), None)

    @api.depends('expected_price')
    def _compute_minimum_sale_price(self):
        for record in self:
            record.minimum_sale_price = record.expected_price * 0.9

    @staticmethod
    def _fsm_can_transition(src_state, dst_state):
        return (src_state, dst_state) not in [
            ('sold', 'canceled'),
            ('canceled', 'sold')
        ]

    def update_state(self):
        """
        Updates the state of the property based on the list/state of existing offers.
        """
        for record in self:
            # only the buttons change stuff to sold and canceled states
            if record.state == 'sold' or record.state == 'canceled':
                continue

            exist_offers = bool(record.offer_ids)
            exist_accepted_offers = exist_offers and any(
                offer.status == 'accepted' for offer in record.mapped('offer_ids'))

            if not exist_offers:
                record.state = 'new'
            elif not exist_accepted_offers:
                record.state = 'offer_received'
            else:
                record.state = 'offer_accepted'

    def action_set_sold(self):
        for record in self:
            record.state = 'sold'
        return True

    def action_set_cancel(self):
        for record in self:
            record.state = 'canceled'
        return True

    def is_deletable(self):
        return all(record.state in ('new', 'canceled') for record in self)

    @api.model
    def write(self, vals):
        # validate fsm state transition
        if dst_state := vals.get('state', None):
            for src_state in self.mapped('state'):
                if not self._fsm_can_transition(src_state, dst_state):
                    raise UserError(_("Invalid state transition from %s to %s", src_state, dst_state))

        return super().write(vals)

    @api.ondelete(at_uninstall=False)
    def _check_if_deletable(self):
        if not self.is_deletable():
            raise UserError("Cannot delete record")
