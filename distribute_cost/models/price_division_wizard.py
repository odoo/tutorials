
from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError
from odoo.tools import float_round


class PriceDivisionWizard(models.TransientModel):
    _name = "price.division.wizard"
    _description = "Price Division Wizard"

    sale_order_id = fields.Many2one('sale.order', string='Sale Order', readonly=True)  # order id
    sale_order_line_id = fields.Many2one('sale.order.line', string='distributed order line')  # order line id which cost is distributed
    remaining_order_line_ids = fields.One2many('price.division.wizard.line', 'wizard_id')  # order line ids where cost is distributed

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        sale_order_line_id = self.env.context.get('active_id')   # fatch oeder line which is distributed
        sale_order_line = self.env['sale.order.line'].browse(sale_order_line_id)

        # if order line exist
        if sale_order_line:
            # filter out remaining all order lines except current for display on wizard
            remaining_order_lines = sale_order_line.order_id.order_line.filtered(
                lambda l: l.id != sale_order_line.id
            )

        division_price = sale_order_line.price_subtotal  # total distributed cost by default
        remaining_lines_count = len(remaining_order_lines)
        remaining_lines_data = []  # list for storing remaining line data

        # if other line exist
        if remaining_lines_count > 0:
            # for eually distribute cost to each remaining order line
            amount_per_line = float_round(division_price / remaining_lines_count if remaining_lines_count else 0.0, precision_digits=2)

            remaining_lines_data = [
                (
                0, 0, {
                        'sale_order_line_id': line.id,
                        'amount': amount_per_line,
                        'is_selected': True,
                    },
                )
                for line in remaining_order_lines
            ]
        else:
            raise UserError("No lines to division price")
        res.update({
            'sale_order_line_id': sale_order_line.id,
            'remaining_order_line_ids': remaining_lines_data,
        })
        return res

    # handle action of divide function
    def action_divide(self):
        for record in self:
            if not record.remaining_order_line_ids:
                return
            sale_order_line = self.env['sale.order.line'].browse(self.env.context.get('active_id'))  # fatch distributed order line
            division_price = sale_order_line.price_subtotal  # possible maximum distribution cost
            total_divided_amount = sum(record.remaining_order_line_ids.mapped("amount"))  # total distributed amount

            if total_divided_amount > division_price:
                raise ValidationError(f"Total shared amount cannot exceed the original line's price as total share amount is {total_divided_amount} and distributed sale order line's price {division_price}")

            # set division price of distributed line is Zero
            sale_order_line.division_price = 0.0
            # add distributed amount to subtotal for all selected order lines
            for line in record.remaining_order_line_ids:
                if line.is_selected:
                    line.sale_order_line_id.write({
                        'division_price': line.amount,
                        'price_subtotal': line.sale_order_line_id.price_subtotal + line.amount,
                        'distributed_line': sale_order_line.id,
                    })
            # remaining amount : not distributed amount
            remaining_amount = round(division_price - total_divided_amount, 2)

            # distributed line assign remainig value to itself so that assign distributed line itself
            sale_order_line.distributed_line = sale_order_line.id
            if remaining_amount > 0:
                sale_order_line.write({
                    'division_price': remaining_amount,
                    'price_subtotal': remaining_amount
                })
                # sale_order_line.division_price = remaining_amount
                # sale_order_line.price_subtotal = remaining_amount
            else:
                sale_order_line.write({
                    'division_price': 0.0,
                    'price_subtotal': 0.0
                })
                sale_order_line.order_id.isDivisionVisible = True


# contain remaining line's indivudual data
class PriceDivisionWizardLine(models.TransientModel):
    _name = "price.division.wizard.line"
    _description = "Price Division Wizard Line"

    wizard_id = fields.Many2one('price.division.wizard')
    sale_order_line_id = fields.Many2one('sale.order.line')
    is_selected = fields.Boolean(string='salected')
    amount = fields.Float(string='Amount')

    @api.onchange('is_selected', 'wizard_id')
    def _onchange_is_selected(self):
        if not self.is_selected:
            self.amount = 0.0
