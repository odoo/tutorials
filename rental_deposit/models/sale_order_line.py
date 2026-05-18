from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_deposit_line = fields.Boolean(default=False)
    parent_rental_line_id = fields.Many2one(
        'sale.order.line',
        string="Parent Rental Line",
        ondelete="cascade",
        index=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        rental_lines = lines.filtered(
            lambda l: l.product_id.rent_ok
            and l.product_id.requires_deposit
            and l.product_id.deposit_amount > 0
            and not l.is_deposit_line
        )
        if not rental_lines:
            return lines
        company_map = {}
        for line in rental_lines:
            company = line.company_id
            if company not in company_map:
                if not company.deposit_product:
                    raise UserError("Please set deposit product in settings.")
                company_map[company] = company.deposit_product
        deposit_vals = []
        for line in rental_lines:
            deposit_product = company_map[line.company_id]
            deposit_vals.append({
                'order_id': line.order_id.id,
                'product_id': deposit_product.id,
                'product_uom_qty': line.product_uom_qty,
                'price_unit': line.product_id.deposit_amount,
                'name': f"Deposit fee for product: {line.product_id.name}",
                'is_deposit_line': True,
                'parent_rental_line_id': line.id,
            })
        self.create(deposit_vals)
        return lines

        # deposit_vals = []
        # for line in rental_lines:
        #     deposit_product = line.company_id.deposit_product
        #     if not deposit_product:
        #         raise UserError("Please set deposit product in settings.")
        #     deposit_vals.append({
        #         'order_id': line.order_id.id,
        #         'product_id': deposit_product.id,
        #         'product_uom_qty': line.product_uom_qty,
        #         'price_unit': line.product_id.deposit_amount,
        #         'name': f"Deposit fee for product: {line.product_id.name}",
        #         'is_deposit_line': True,
        #         'parent_rental_line_id': line.id,
        #     })
        # self.create(deposit_vals)
        # return lines

    @api.ondelete(at_uninstall=False)
    def _unlink_deposit_fee(self):
        if not self.env.context.get("bypass_deposit_protection_for_delete"):
            for record in self:
                if record.is_deposit_line:
                    raise UserError("You can't delete a Deposit Product line directly.")

    def write(self, vals):
        if not self.env.context.get("bypass_deposit_protection_for_write"):
            for record in self:
                if record.is_deposit_line:
                    raise UserError("You can't edit Deposit Product line directly.")
        res = super().write(vals)
        if 'product_uom_qty' not in vals:
            return res
        rental_lines = self.filtered(
            lambda l: l.product_id.rent_ok
            and l.product_id.requires_deposit
            and l.product_id.deposit_amount > 0
            and not l.is_deposit_line
        )
        for line in rental_lines:
            deposit_line = self.search([('parent_rental_line_id', '=', line.id)], limit=1)
            if deposit_line:
                deposit_line.with_context(bypass_deposit_protection_for_write=True).write({
                    'product_uom_qty': line.product_uom_qty,
                    'price_unit': line.product_id.deposit_amount,
                })
        return res
