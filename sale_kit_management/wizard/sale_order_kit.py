from odoo import api, fields, models


class SaleOrderKitLine(models.TransientModel):
    _name = 'sale.order.kit.line'
    _description = "Kit Wizard Line"

    wizard_id = fields.Many2one('sale.order.kit', ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product", required=True)
    kit_unit_qty = fields.Float(string="Kit Unit Qty", default=1.0)
    price_unit = fields.Float(string="Price")
    amount = fields.Float(string="Amount", compute='_compute_amount', store=True)

    @api.depends('kit_unit_qty', 'price_unit')
    def _compute_amount(self):
        for line in self:
            line.amount = line.kit_unit_qty * line.price_unit


class SaleOrderKit(models.TransientModel):
    _name = 'sale.order.kit'
    _description = "Kit Configurator Wizard"

    _KIT_SUBPRODUCT_SEQ_BASE = 200

    sale_order_line_id = fields.Many2one('sale.order.line', required=True)
    parent_product = fields.Many2one(
        'product.product',
        string="Product",
        compute='_compute_parent_product',
    )
    kit_line_ids = fields.One2many('sale.order.kit.line', 'wizard_id', string="Sub Products")
    kit_total_price = fields.Float(
        string="Kit Price",
        compute='_compute_kit_total_price',
    )
    has_kit_subproducts = fields.Boolean(compute='_compute_has_kit_subproducts')

    @api.depends('sale_order_line_id.product_id')
    def _compute_parent_product(self):
        for rec in self:
            rec.parent_product = rec.sale_order_line_id.product_id

    @api.depends('kit_line_ids.price_unit', 'kit_line_ids.kit_unit_qty')
    def _compute_kit_total_price(self):
        for rec in self:
            rec.kit_total_price = sum(
                line.price_unit * line.kit_unit_qty
                for line in rec.kit_line_ids
            )

    @api.depends('sale_order_line_id.has_kit_subproducts')
    def _compute_has_kit_subproducts(self):
        for rec in self:
            rec.has_kit_subproducts = rec.sale_order_line_id.has_kit_subproducts

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        sol_id = self.env.context.get('default_sale_order_line_id')
        if sol_id:
            sol = self.env['sale.order.line'].browse(sol_id)

            if sol.kit_config_line_ids:
                lines = [(0, 0, {
                    'product_id': line.product_id.id,
                    'kit_unit_qty': line.kit_unit_qty,
                    'price_unit': line.price_unit,
                }) for line in sol.kit_config_line_ids]

            else:
                product_tmpl = sol.product_id.product_tmpl_id
                lines = [(0, 0, {
                    'product_id': sub.product_id.id,
                    'kit_unit_qty': sub.kit_unit_qty,
                    'price_unit': sub.price_unit,
                }) for sub in product_tmpl.subproduct_ids]

            res['kit_line_ids'] = lines
        return res

    def action_confirm(self):
        self.ensure_one()
        sol = self.sale_order_line_id

        sol.kit_config_line_ids.unlink()
        config_vals = [{
            'sale_order_line_id': sol.id,
            'product_id': line.product_id.id,
            'kit_unit_qty': line.kit_unit_qty,
            'price_unit': line.price_unit,
        } for line in self.kit_line_ids]
        self.env['sale.order.kit.config.line'].create(config_vals)

        sol.price_unit = sum(
            line.price_unit * line.kit_unit_qty
            for line in self.kit_line_ids
        )

        return {'type': 'ir.actions.act_window_close'}

    def action_add_to_sol(self):
        self.ensure_one()
        sol = self.sale_order_line_id
        order = sol.order_id
        product_name = sol.product_id.display_name

        sol.kit_config_line_ids.unlink()
        config_vals = [{
            'sale_order_line_id': sol.id,
            'product_id': line.product_id.id,
            'kit_unit_qty': line.kit_unit_qty,
            'price_unit': line.price_unit,
        } for line in self.kit_line_ids]
        self.env['sale.order.kit.config.line'].create(config_vals)

        sol.price_unit = sum(
            line.price_unit * line.kit_unit_qty
            for line in self.kit_line_ids
        )

        existing_kit_sections = order.order_line.filtered(
            lambda l: l.display_type == 'line_section' and l.kit_parent_line_id
        )
        max_sequence = max(seq.sequence
                           for seq in existing_kit_sections
                           ) if existing_kit_sections else 0

        base_seq = self._KIT_SUBPRODUCT_SEQ_BASE + max_sequence * 2

        child_lines = self.env['sale.order.line'].search([
            ('kit_parent_line_id', 'in', sol.id),
            ('id', 'not in', sol.id),
        ])
        if child_lines:
            for line in child_lines:
                if line.display_type == 'line_section':
                    base_seq = line.sequence
            child_lines.unlink()

        self.env['sale.order.line'].create({
            'order_id': order.id,
            'display_type': 'line_section',
            'name': f"Subproducts of {product_name}",
            'sequence': base_seq,
            'kit_parent_line_id': sol.id,
        })

        for idx, line in enumerate(self.kit_line_ids, start=1):
            self.env['sale.order.line'].create({
                'order_id': order.id,
                'product_id': line.product_id.id,
                'product_uom_qty': line.kit_unit_qty * sol.product_uom_qty,
                'price_unit': 0,
                'sequence': base_seq + idx,
                'is_kit_subproduct': True,
                'kit_parent_line_id': sol.id,
                'kit_unit_qty': line.kit_unit_qty,
            })

        return {'type': 'ir.actions.act_window_close'}
