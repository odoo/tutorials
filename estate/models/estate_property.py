from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare

class homePlan(models.Model):
    _name = 'estate.property'
    _description = "this is home plan"
    _order = "id desc"

    name = fields.Char("Plan Name", required=True, default="Unknown")
    description = fields.Char("Description")
    postcode = fields.Char("Post code", required=True)
    date_availability = fields.Datetime(
        "Available till",
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
    )
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    expected_price = fields.Float("Expected Price")
    selling_price = fields.Float("Selling price", copy=False, readonly=True)
    bedrooms = fields.Integer("bedrooms", default=2)
    living_area = fields.Integer("Living area")
    facades = fields.Integer("facades")
    garage = fields.Boolean("Garage", default=True)
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden area", default=0)
    total_area = fields.Float("Total area", compute='_compute_total_area', store=True)
    best_price = fields.Float("Best price", compute='_compute_best_price', store=True)
    total_maintenance_cost = fields.Float( compute='_compute_total_maintenance', store=True)
    active = fields.Boolean("Active", default=True)
    property_type_id = fields.Many2one("estate.property.type")
    salesman_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", copy=False)
    property_tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    sequence = fields.Integer('Sequence', help="Used to order stages. Lower is better.")
    maintenance_ids = fields.One2many("estate.property.maintenance", "property_id")
    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer received"),
            ('offer_accepted', "Offer accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        default='new',
        copy=False,
    )

    garden_orientation_direction = fields.Selection(
        [('north', "North"), ('east', "East"), ('west', "West"), ('south', "South")]
    )

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)', "The expected price must be Strictly positive"
    )
    _check_property_selling_price = models.Constraint(
        'CHECK(selling_price > 0)', "The expected price must be Strictly positive"
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for line in self:
            line.total_area = line.living_area + line.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)

    @api.onchange('garden')
    def _onchange_partner(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation_direction = 'east'

            else:
                record.garden_area = 0
                record.garden_orientation_direction = False

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price and float_compare(
                record.selling_price, (0.9 * record.expected_price)
                ,2 ) == -1 :
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price."
                )

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(message="You can't sold once you have cancelled")
            elif record.maintenance_ids.filtered(lambda r : r.status != 'Done'):
                raise UserError("maintamce remain")   
            else:
                record.state = 'sold'
        return True

    def action_Cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(message="You can't Cancel once you have sold")
            else:
                record.state = 'cancelled'

        return True

    @api.depends('maintenance_ids.cost')
    def _compute_total_maintenance(self):
        for record in self:
            record.total_maintenance_cost = sum(record.maintenance_ids.mapped('cost'))

            