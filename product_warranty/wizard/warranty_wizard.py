from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AddWarrantyLinesWizard(models.TransientModel):
    _name = "add.warranty.lines.wizard"
    _description = "Warranty Line Wizard"

    wizard_id = fields.Many2one('add.warranty.wizard', string="Wizard Reference", ondelete="cascade")
    product_id = fields.Many2one(comodel_name="product.product", string="Product")
    sale_order_line_id = fields.Many2one(comodel_name="sale.order.line", string="Sale Order Line")
    warranty_name = fields.Many2one(comodel_name="warranty.config", string="Warranty Configuration")
    end_date = fields.Date(readonly=True, string="End Date", compute="_compute_end_date")

    @api.depends('warranty_name')
    def _compute_end_date(self):
        for record in self:
            if record.warranty_name:
                # Calculate the warranty end date based on the period in years
                record.end_date = fields.Date.today() + relativedelta(years=record.warranty_name.period)
            else:
                record.end_date = False


class AddWarrantyWizard(models.TransientModel):
    _name = "add.warranty.wizard"
    _description = "Add Warranty Wizard"

    # This field will hold the warranty lines for products
    wizard_line_ids = fields.One2many(
        comodel_name='add.warranty.lines.wizard',
        inverse_name='wizard_id',
        string="Warranty Lines"
    )

    # Default get method to populate the wizard with sale order lines eligible for warranty
    # res is dictionary to store the default value
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        # Get the sale order ID from the context, id was passed in sale_order.py open_warranty_wizard function
        sale_order = self.env['sale.order'].browse(self.env.context.get("default_sale_order_id"))

        # Get sale order lines with warranty available and not yet having a warranty
        sale_order_lines = sale_order.order_line.filtered(
            lambda line: line.product_id.is_warranty_available and not line.has_warranty
        )

        # Populate the wizard lines
        res.update({
                'wizard_line_ids': [(0, 0, {
                'sale_order_line_id': line.id,
                'product_id': line.product_id.id,
            }) for line in sale_order_lines]
        })
        return res

    # Action to add warranty for the products
    def action_add(self):
        sale_order_line = self.env['sale.order.line']
        warranty_lines = self.wizard_line_ids

        for line in warranty_lines:
            if line.warranty_name:
                # Create a new sale order line for warranty
                sale_order_line.create({
                    'order_id': line.sale_order_line_id.order_id.id,
                    'product_id':  line.warranty_name.product.id,  # warranty product
                    'product_uom_qty': 1,
                    'price_unit': line.warranty_name.percentage / 100 * line.sale_order_line_id.price_unit,  # price based on percentage
                    'name': f"{line.sale_order_line_id.product_id.name} Warranty, End Date: {line.end_date}",
                    'order_line_linked_to_warranty': line.sale_order_line_id.id,
                    'is_warranty': True,
                })

                # Update the original sale order line to mark it as having a warranty
                line.sale_order_line_id.write({'has_warranty': True})
        return True
