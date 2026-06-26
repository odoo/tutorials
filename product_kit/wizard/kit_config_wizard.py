from odoo import api, fields, models
from odoo.tools.translate import _


class KitConfigWizard(models.TransientModel):
    _name = 'kit.config.wizard'
    _description = 'Kit Configuration Wizard'

    sale_order_id = fields.Many2one(
        'sale.order',
        string="Sale Order",
        required=True,
    )
    sale_line_id = fields.Many2one(
        'sale.order.line',
        string="Sale Order Line",
        required=True,
    )

    # Display fields
    product_id = fields.Many2one(
        'product.product',
        string="Product",
        related='sale_line_id.product_id',
        readonly=True,
    )
    product_image = fields.Binary(
        string="Product Image",
        related='sale_line_id.product_id.image_1920',
        readonly=True,
    )
    product_name = fields.Char(
        string="Product Name",
        related='sale_line_id.product_id.display_name',
        readonly=True,
    )
    order_name = fields.Char(
        string="Order",
        related='sale_order_id.name',
        readonly=True,
    )
    kit_quantity = fields.Float(
        string="Kit Quantity",
        related='sale_line_id.product_uom_qty',
        readonly=True,
    )

    line_ids = fields.One2many(
        'kit.config.wizard.line',
        'wizard_id',
        string="Kit Lines",
    )

    @api.model
    def default_get(self, fields_list):
        res = super(KitConfigWizard, self).default_get(fields_list)
        active_id = self.env.context.get('active_id')
        sale_line_id = self.env.context.get('default_sale_line_id') or active_id

        if sale_line_id:
            line = self.env['sale.order.line'].browse(sale_line_id)
            res.update({
                'sale_line_id': sale_line_id,
                'sale_order_id': line.order_id.id,
            })

            kit_template = line.product_id.product_tmpl_id
            if kit_template.is_kit and kit_template.kit_product_ids:
                kit_lines = [(0, 0, {
                    'product_id': k.product_id.id,
                    'quantity': k.quantity * line.product_uom_qty,
                    'price_unit': k.product_id.lst_price,
                }) for k in kit_template.kit_product_ids]
                res['line_ids'] = kit_lines

        return res

    def action_confirm(self):
        self.ensure_one()
        line = self.sale_line_id

        if line.kit_line_ids:
            line.kit_line_ids.unlink()

        section_seq = line.sequence + 1
        section_line = self.env['sale.order.line'].create({
            'order_id': self.sale_order_id.id,
            'display_type': 'line_section',
            'name': _("Sub products of %s", line.name or line.product_id.display_name),
            'sequence': section_seq,
        })

        for idx, wizard_line in enumerate(self.line_ids):
            vals = {
                'order_id': self.sale_order_id.id,
                'product_id': wizard_line.product_id.id,
                'product_uom_qty': wizard_line.quantity,
                'price_unit': wizard_line.price_unit,
                'name': wizard_line.product_id.display_name,
                'parent_kit_line_id': line.id,
                'sequence': section_seq + 1 + idx,
            }
            new_line = self.env['sale.order.line'].create(vals)
            line.write({'kit_line_ids': [(4, new_line.id)]})

        vals = {'product_uom_qty': 0}
        if line.name and not line.name.startswith('[Kit] '):
            vals['name'] = f"[Kit] {line.name}"
        line.write(vals)

        return {'type': 'ir.actions.act_window_close'}
