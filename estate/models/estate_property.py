from odoo import api,models, fields,modules
from datetime import timedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_is_zero, float_compare

class EstateProperty(models.Model): 
    _name        = "estate.property"
    _description = "Bất động Sản"

    name              = fields.Char(string="Title", required=True)
    description       = fields.Text(string="Description")
    postcode          = fields.Integer(string="Postcode")
    date_availability = fields.Datetime(
        string  = "Available From",
        copy    = False,
        default = lambda self: fields.Datetime.now() + timedelta(days=90),
    )
    expected_price     = fields.Float(string="Expected Price", required=True, default=0)
    selling_price      = fields.Float(string="Selling Price", copy=False)
    bedrooms           = fields.Integer(string="Bedrooms", default=2)
    living_area        = fields.Integer(string="Living Area (sqm)")
    facades            = fields.Integer(string="Facades")
    garage             = fields.Boolean(string="Garage", default=True)
    garden             = fields.Boolean(string="Garden", default=True)
    garden_area        = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string    = "Garden Orientation",
        selection = [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help = "Type is used to separate North, South, East, West",
    )
    is_active = fields.Boolean( string="Active", default=False)
    state     = fields.Selection(
        string    = "State",
        selection = [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new"
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id         = fields.Many2one("res.partner", string = "Buyer", copy = False)
    seller_id        = fields.Many2one("res.users", string = "Vendor", default = lambda self: self.env.user )
    tag_ids          = fields.Many2many("estate.property.tag",)
    offer_ids        = fields.One2many("estate.property.offer", "property_id")
    _order = "id desc"
    
    total_area = fields.Float(compute="_compute_area", digits=(16, 0))
    best_price = fields.Float(string="Best price", compute="_compute_best_price", digits=(16,0))

    property_ids = fields.Many2one("estate.property.type")

    salesperson_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    
    @api.depends("living_area" , "garden_area")
    def _compute_area(self): 
     for record in self     : 
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
         price = record.offer_ids.mapped("price")
         record.best_price = max(price) if price else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
          self.garden_area = 10 if self.garden else 0
          self.garden_orientation = "north" if self.garden else False

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError('Không thể bán trạng thái cancel')
            record.state = "sold"
        return True
        
    def action_cancel(self):
        for record in self:
            if record.state == "sold":
               raise UserError('Không thể cancel trạng thái sold')
            record.state = "cancelled"
        return True

    _sql_constraints = [
    ('check_expected_price', 'CHECK(expected_price > 0)', 'Giá kỳ vọng phải là số dương!'),
    ('check_selling_price', 'CHECK(selling_price >= 0)', 'Giá bán phải là số dương!'),
    ('unique_name', 'UNIQUE(name,description)', 'Tên không được trùng')
    ]
    @api.constrains('selling_price','expected_price')
    def _check_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits = 2):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits = 2) == -1:
                    raise ValidationError('Giá bán không được thấp hơn 90% giá kỳ vọng')
            
    @api.ondelete(at_uninstall=False)
    def onDelete(self):
     for record in self:
        if record.state not in ('new', 'cancelled'):
            raise UserError("Chỉ có thể xóa ở trạng thái Mới hoặc Đã hủy!")


       
