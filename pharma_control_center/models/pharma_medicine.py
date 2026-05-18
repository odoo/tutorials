from datetime import date, timedelta, datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError



class PharmacyMedicine(models.Model):
    _name = "pharmacy.medicine"
    _description = "Pharmacy Medicine"
    _order = "name"

    name = fields.Char(string="Medicine Name", required=True)
    description = fields.Text(string="Description")
    manufacturer = fields.Char(string="Manufacturer")
    barcode = fields.Char(string="Barcode")
    category_id = fields.Many2one('pharmacy.category', string="Medicine Category", required=True, ondelete='restrict')
    sub_category = fields.Char(string="Sub‑Category")
    batch_number = fields.Char(string="Batch Number", required=True)
    expiry_date = fields.Date(string="Expiry Date", required=True)
    price = fields.Float(string="Selling Price", required=True)
    cost_price = fields.Float(string="Cost Price")
    profit_margin = fields.Float(string="Profit Margin (%)", compute="_compute_profit_margin", store=True)
    quantity = fields.Integer(string="Stock Quantity", required=True, default=0)
    reorder_level = fields.Integer(string="Reorder Level", default=10)
    need_reorder = fields.Boolean(string="Need Reorder", compute="_compute_need_reorder", store=True)
    order_qty = fields.Integer(string="Order Quantity", default=1)
    in_stock = fields.Boolean(string="In Stock", compute="_compute_in_stock", store=True)
    days_to_expiry = fields.Integer(string="Days to Expiry", compute="_compute_expiry_days", store=True)
    expiry_status = fields.Selection([
        ('fresh', 'Fresh'),
        ('expiring_soon', 'Expiring Soon'),
        ('expired', 'Expired'),
    ], string="Expiry Status", compute="_compute_expiry_status", store=True)
    storage_location = fields.Selection([
        ('room_temp', 'Room Temperature'),
        ('cold', 'Cold Storage'),
        ('frozen', 'Frozen'),
    ], string="Storage Condition", required=True)
    side_effects = fields.Text(string="Side Effects")
    dosage = fields.Char(string="Dosage")
    license_category = fields.Selection([
        ('green', '🟢 Pharmacy (Category A) - Full license'),
        ('blue', '🔵 Medical Store (Category B) - Limited license'),
        ('white', '⚪ Drug Store (Category C) - Basic OTC'),
    ], string="Pharmacy License Category", required=True, default='white')
    product_id = fields.Many2one('product.product', string="Linked Product", readonly=True)
    last_sale_order_id = fields.Many2one('sale.order', string="Last Sale Order", readonly=True)
    last_invoice_id = fields.Many2one('account.move', string="Last Invoice", readonly=True)
    today_orders_qty = fields.Float(string="Today Orders", compute="_compute_today_orders", store=False)

    # ------------------------------------------------------------
    # Cart actions (using dedicated cart model)
    # ------------------------------------------------------------
    def add_to_cart(self):
        self.ensure_one()
        if self.order_qty <= 0:
            raise UserError(_("Order quantity must be greater than zero."))
        if self.order_qty > self.quantity:
            raise UserError(_("Not enough stock. Available: %s", self.quantity))

        cart = self.env['pharmacy.cart'].search([('user_id', '=', self.env.user.id)], limit=1)
        if not cart:
            cart = self.env['pharmacy.cart'].create({'user_id': self.env.user.id})

        cart_line = self.env['pharmacy.cart.line'].search([
            ('cart_id', '=', cart.id),
            ('medicine_id', '=', self.id)
        ], limit=1)
        if cart_line:
            cart_line.quantity += self.order_qty
        else:
            self.env['pharmacy.cart.line'].create({
                'cart_id': cart.id,
                'medicine_id': self.id,
                'quantity': self.order_qty,
            })
        self.order_qty = 1
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Added to Cart'),
                'message': _("Added %s to your cart.", self.name),
                'type': 'success',
                'sticky': False,
            }
        }

    # ------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------
    def _create_product(self):
        product = self.env['product.product'].create({
            'name': self.name,
            'list_price': self.price,
            'standard_price': self.cost_price or 0.0,
            'type': 'consu',
            'sale_ok': True,
            'purchase_ok': False,
        })
        self.product_id = product
        return product

    # ------------------------------------------------------------
    # Compute methods (unchanged)
    # ------------------------------------------------------------
    @api.depends('price', 'cost_price')
    def _compute_profit_margin(self):
        for med in self:
            if med.cost_price and med.cost_price > 0:
                med.profit_margin = ((med.price - med.cost_price) / med.cost_price) * 100
            else:
                med.profit_margin = 0.0

    @api.depends('quantity', 'reorder_level')
    def _compute_need_reorder(self):
        for med in self:
            med.need_reorder = med.quantity <= med.reorder_level

    @api.depends('quantity')
    def _compute_in_stock(self):
        for med in self:
            med.in_stock = med.quantity > 0

    @api.depends('expiry_date')
    def _compute_expiry_days(self):
        today = date.today()
        for med in self:
            if med.expiry_date:
                delta = (med.expiry_date - today).days
                med.days_to_expiry = delta
            else:
                med.days_to_expiry = 0

    @api.depends('expiry_date')
    def _compute_expiry_status(self):
        today = date.today()
        for med in self:
            if not med.expiry_date:
                med.expiry_status = 'fresh'
            elif med.expiry_date < today:
                med.expiry_status = 'expired'
            elif med.expiry_date <= today + timedelta(days=30):
                med.expiry_status = 'expiring_soon'
            else:
                med.expiry_status = 'fresh'

    @api.depends('product_id')
    def _compute_today_orders(self):
        today_start = datetime.now().replace(hour=0, minute=0, second=0)
        today_end = today_start + timedelta(days=1)
        for med in self:
            total = 0.0
            if med.product_id:
                lines = self.env['sale.order.line'].search([
                    ('product_id', '=', med.product_id.id),
                    ('order_id.date_order', '>=', today_start),
                    ('order_id.date_order', '<', today_end),
                    ('order_id.state', 'not in', ['cancel'])
                ])
                total = sum(lines.mapped('product_uom_qty'))
            med.today_orders_qty = total

