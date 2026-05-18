from odoo import _, api, fields, models
from odoo.exceptions import UserError



class PharmacyCart(models.Model):
    _name = "pharmacy.cart"
    _description = "Shopping Cart"
    _rec_name = "user_id"

    user_id = fields.Many2one('res.users', string="User", required=True, default=lambda self: self.env.user)
    cart_line_ids = fields.One2many('pharmacy.cart.line', 'cart_id', string="Cart Lines")
    total_quantity = fields.Integer(string="Total Quantity", compute="_compute_totals")
    total_amount = fields.Float(string="Total Amount", compute="_compute_totals")

    # Quick add fields
    quick_medicine_ids = fields.Many2many('pharmacy.medicine', string="Add Medicines")
    quick_order_qty = fields.Integer(string="Order Quantity", default=1)

    # Barcode input (temporary, not stored)
    barcode_input = fields.Char(string="Barcode", help="Scan or type medicine barcode to add to cart")

    # Drug interaction warnings (displayed in the form)
    interaction_warnings = fields.Text(string="Interactions", compute="_compute_interaction_warnings")

    @api.depends('cart_line_ids.subtotal')
    def _compute_totals(self):
        for cart in self:
            cart.total_quantity = sum(cart.cart_line_ids.mapped('quantity'))
            cart.total_amount = sum(cart.cart_line_ids.mapped('subtotal'))

    @api.depends('cart_line_ids.medicine_id')
    def _compute_interaction_warnings(self):
        for cart in self:
            medicines = cart.cart_line_ids.mapped('medicine_id')
            if len(medicines) < 2:
                cart.interaction_warnings = False
                continue
            interactions = self.env['pharmacy.interaction'].search([
                ('medicine1_id', 'in', medicines.ids),
                ('medicine2_id', 'in', medicines.ids)
            ])
            if interactions:
                warnings = [f"{i.medicine1_id.name} + {i.medicine2_id.name}: {i.warning_text}" for i in interactions]
                cart.interaction_warnings = "\n".join(warnings)
            else:
                cart.interaction_warnings = False

    def _check_interactions(self):
        """Return list of interaction dicts for current cart lines."""
        medicines = self.cart_line_ids.mapped('medicine_id')
        if len(medicines) < 2:
            return []
        interactions = self.env['pharmacy.interaction'].search([
            ('medicine1_id', 'in', medicines.ids),
            ('medicine2_id', 'in', medicines.ids)
        ])
        return [{
            'medicine1': inter.medicine1_id.name,
            'medicine2': inter.medicine2_id.name,
            'severity': inter.severity,
            'warning': inter.warning_text,
        } for inter in interactions]

    def action_add_quick_medicines(self):
        for cart in self:
            if cart.quick_medicine_ids and cart.quick_order_qty > 0:
                for med in cart.quick_medicine_ids:
                    line = self.env['pharmacy.cart.line'].search([
                        ('cart_id', '=', cart.id),
                        ('medicine_id', '=', med.id)
                    ], limit=1)
                    if line:
                        line.quantity += cart.quick_order_qty
                    else:
                        self.env['pharmacy.cart.line'].create({
                            'cart_id': cart.id,
                            'medicine_id': med.id,
                            'quantity': cart.quick_order_qty,
                        })
                cart.quick_medicine_ids = False
                cart.quick_order_qty = 1
        return {'type': 'ir.actions.client', 'tag': 'reload'}

    def action_add_by_barcode(self):
        """Add medicine to cart by scanning/entering its barcode."""
        self.ensure_one()
        barcode = self.barcode_input
        if not barcode:
            raise UserError(_("Please scan or enter a barcode."))
        medicine = self.env['pharmacy.medicine'].search([('barcode', '=', barcode)], limit=1)
        if not medicine:
            raise UserError(_("No medicine found with barcode %s.", barcode))
        if medicine.quantity <= 0:
            raise UserError(_("Medicine %s is out of stock.", medicine.name))
        line = self.env['pharmacy.cart.line'].search([
            ('cart_id', '=', self.id),
            ('medicine_id', '=', medicine.id)
        ], limit=1)
        if line:
            line.quantity += 1
        else:
            self.env['pharmacy.cart.line'].create({
                'cart_id': self.id,
                'medicine_id': medicine.id,
                'quantity': 1,
            })
        self.barcode_input = False
        return {'type': 'ir.actions.client', 'tag': 'reload'}

    def action_checkout(self):
        self.ensure_one()
        if not self.cart_line_ids:
            raise UserError(_("Your cart is empty."))

        # Check for ANY interaction and block checkout
        interactions = self._check_interactions()
        if interactions:
            warnings = "\n".join([f"{i['medicine1']} + {i['medicine2']}: {i['warning']}" for i in interactions])
            raise UserError(_(
                "Drug Interaction Warning!\n\n%s\n\nPlease remove conflicting medicines or contact your doctor.",
                warnings,
            ))

        order_lines = []
        for line in self.cart_line_ids:
            if not line.medicine_id.product_id:
                line.medicine_id._create_product()
            order_lines.append((0, 0, {
                'product_id': line.medicine_id.product_id.id,
                'product_uom_qty': line.quantity,
                'price_unit': line.medicine_id.price,
            }))
        sale_order = self.env['sale.order'].create({
            'partner_id': self.env.user.partner_id.id,
            'order_line': order_lines,
        })
        sale_order.action_confirm()
        invoice = sale_order._create_invoices()
        invoice.action_post()
        for line in self.cart_line_ids:
            line.medicine_id.quantity -= line.quantity
        self.cart_line_ids.unlink()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'new',
        }


class PharmacyCartLine(models.Model):
    _name = "pharmacy.cart.line"
    _description = "Cart Line"
    _rec_name = "medicine_id"

    cart_id = fields.Many2one('pharmacy.cart', string="Cart", required=True, ondelete='cascade')
    medicine_id = fields.Many2one('pharmacy.medicine', string="Medicine", required=True)
    quantity = fields.Integer(string="Quantity", required=True, default=1)
    unit_price = fields.Float(string="Unit Price", related='medicine_id.price', readonly=True)
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_price

