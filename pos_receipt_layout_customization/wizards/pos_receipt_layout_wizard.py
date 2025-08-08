from odoo import api, fields, models


class PosReceiptLayoutWizard(models.TransientModel):
    _name = 'pos.receipt.layout.wizard'
    _description = 'POS Receipt Layout Configuration Wizard'

    pos_config_id = fields.Many2one('pos.config', string="POS Config")
    is_restaurant = fields.Boolean(string="Is Restaurant", compute="_compute_is_restaurant")

    receipt_layout = fields.Selection([
        ('light', 'Light'),
        ('lined', 'Lined'),
        ('boxed', 'Boxed'),
    ], string="Layout Style", default='light')

    receipt_logo = fields.Binary(string="Logo", related='pos_config_id.receipt_logo', readonly=False)
    receipt_header = fields.Html(string="Header")
    receipt_footer = fields.Html(string="Footer")
    preview_html = fields.Html(string="Preview", compute="_compute_preview_html")

#     PREVIEW_TEMPLATE = """
#     <t t-name="pos_receipt_layout_customization.pos_receipt_preview_template_render">
#         # <!-- <t t-name="pos_receipt_layout_customization.ReceiptPreview"> -->
#         <t t-call="web.html_container">
#             <div
#                 style="height: 100%; background-color: #f0f0f0; display: flex; justify-content: center; align-items: center; min-height: 100vh;">
#                 <div
#                     style="background-color: white; padding: 20px; height: 100%; width: 80%; max-width: 1100px; font-family: Arial, sans-serif; font-size: 25px; text-align: center; ">

#                     <div class="text-center" style="margin-bottom: 10px;">
#                         <t t-if="logo" class="o_company_logo_big">
#                             <img t-att-src="image_data_uri(logo)"
#                                 style="max-height: 100px; margin-bottom: 25px;" alt="Logo" />
#                         </t>

#                         <!-- <div class="d-inline-block mb-1">
#                                 <img t-if="receipt_logo" t-att-src="image_data_uri(receipt_logo)" alt="Logo" class="img-fluid"
#                             style="max-width: 60px; height: auto;"/>
#                             </div> -->
#                         <br />
#                         <div
#                             style="text-align: center; margin-top: 10px; font-size: 20px; font-weight: 500;">Odoo
#                             India Pvt Ltd.<br /> Infocity, Gandhinagar<br /> Tax ID: 2233009900223</div>

#                         <div style="margin-top: 10px; text-align: center;">
#                             <t t-out="header_html" />
#                         </div>

#                         <br />

#                         <h3 style="text-align: center; margin: 5px 0;">701</h3>
#                         <t t-if="is_restaurant and layout_style in ['lined', 'boxed']">
#                             <p style="text-align: center; margin: 0;">Served By MOG</p>
#                             <p style="text-align: center; margin: 0;">Table 5 Guest 3</p>
#                         </t>
#                     </div>
#                     <br />

#                     <t t-if="layout_style in ['light', 'lined']">
#                         <table
#                             style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
#                             <thead>
#                                 <tr
#                                     style="border-bottom: 3px solid black; background: #f0f0f0; border-bottom: 2px solid #ccc;">
#                                     <th
#                                         style="text-align: left; padding: 5px; font-weight: bold; ">
#                                         No</th>
#                                     <th
#                                         style="text-align: left; padding: 5px; font-weight: bold;">
#                                         Item</th>
#                                     <th
#                                         style="text-align: right; padding: 5px; font-weight: bold;">
#                                         Quantity</th>
#                                     <th
#                                         style="text-align: right; padding: 5px; font-weight: bold;">
#                                         Price</th>
#                                     <th
#                                         style="text-align: right; padding: 5px; font-weight: bold;">
#                                         Amount</th>
#                                 </tr>
#                             </thead>
#                             <tbody>
#                                 <tr style="border-bottom: 2px solid #eee;">
#                                     <td style="padding: 5px;">1</td>
#                                     <td style="padding: 5px;">Margrita Pizza</td>
#                                     <td style="text-align: right; padding: 5px;">3</td>
#                                     <td style="text-align: right; padding: 5px;">200</td>
#                                     <td
#                                         style="text-align: right; padding: 5px; background-color: #f5f5f5;">
#                                         600</td>
#                                 </tr>
#                                 <tr style="border-bottom: 2px solid #eee;">
#                                     <td style="padding: 5px;">2</td>
#                                     <td style="padding: 5px;">Bacon Burger</td>
#                                     <td style="text-align: right; padding: 5px;">5</td>
#                                     <td style="text-align: right; padding: 5px;">150</td>
#                                     <td
#                                         style="text-align: right; padding: 5px; background-color: #f5f5f5;">
#                                         750</td>
#                                 </tr>
#                                 <tr style="border-bottom: 2px solid #eee;">
#                                     <td style="padding: 5px;">3</td>
#                                     <td style="padding: 5px;">Apple Pie</td>
#                                     <td style="text-align: right; padding: 5px;">2</td>
#                                     <td style="text-align: right; padding: 5px;">100</td>
#                                     <td
#                                         style="text-align: right; padding: 5px; background-color: #f5f5f5;">
#                                         200</td>
#                                 </tr>
#                                 <tr style="border-bottom: 2px solid #eee;">
#                                     <td style="padding: 5px;">4</td>
#                                     <td style="padding: 5px;">Cheese Burger</td>
#                                     <td style="text-align: right; padding: 5px;">1</td>
#                                     <td style="text-align: right; padding: 5px;">75</td>
#                                     <td
#                                         style="text-align: right; padding: 5px; background-color: #f5f5f5;">
#                                         75</td>
#                                 </tr>
#                             </tbody>
#                         </table>

#                         <table
#                             style="width: 100%; border-collapse: collapse; font-family: Arial, sans-serif; font-size: 20px;">
#                             <tr>
#                                 <td style="text-align: left; padding: 5px; ">
#                                     <strong>Total Qty:</strong> 11 </td>
#                                 <td
#                                     style="text-align: right; padding: 5px; background-color: #f5f5f5;">
#                                     <strong>Sub-Total:</strong> 1625 </td>
#                             </tr>
#                             <tr>
#                                 <td></td>
#                                 <td
#                                     style="text-align: right; padding: 5px; background-color: #f5f5f5;">
#                                     <strong>Bank:</strong> 1625 </td>
#                             </tr>
#                         </table>

#                         <br />
#                         <hr />
#                         <table style="width: 100%; margin-bottom: 20px;">
#                             <thead>
#                                 <tr
#                                     style="border-top: 4px solid black; border-bottom: 4px solid black;">
#                                     <th
#                                         style="text-align: left; padding: 5px; background: #f0f0f0; border-bottom: 2px solid #ccc;">
#                                         Tax</th>
#                                     <th
#                                         style="text-align: right; padding: 5px; background: #f0f0f0; border-bottom: 2px solid #ccc;">
#                                         Amount</th>
#                                     <th
#                                         style="text-align: right; padding: 5px; background: #f0f0f0; border-bottom: 2px solid #ccc;">
#                                         Base</th>
#                                     <th
#                                         style="text-align: right; padding: 5px; background: #f0f0f0; border-bottom: 2px solid #ccc;
# ">
#                                         Total</th>
#                                 </tr>
#                             </thead>
#                             <!-- <br /> -->
#                             <tbody>
#                                 <tr>
#                                     <td style="text-align: left; padding: 5px;">SGST 2.5%</td>
#                                     <td style="text-align: right; padding: 5px;">40.2 </td>
#                                     <td style="text-align: right; padding: 5px;">1584.8</td>
#                                     <td
#                                         style="text-align: right; padding: 5px; background-color: #f5f5f5;">
#                                         1625</td>
#                                 </tr>
#                                 <tr>
#                                     <td style="text-align: left; padding: 5px;">SGST 2.5%</td>
#                                     <td style="text-align: right; padding: 5px;">40.2 </td>
#                                     <td style="text-align: right; padding: 5px;">1584.8</td>
#                                     <td
#                                         style="text-align: right; padding: 5px; background-color: #f5f5f5;">
#                                         1625</td>
#                                 </tr>
#                             </tbody>
#                         </table>
#                     </t>

#                     <t t-if="layout_style == 'boxed'">
#                         <table
#                             style="width: 100%; border-collapse: collapse; border: 3px solid black; margin-bottom: 20px;">
#                             <thead>
#                                 <tr style="border-bottom: 4px solid black;">
#                                     <th
#                                         style="text-align: center; padding: 8px; border-right: 4px solid black; background: #ddd; width: 10%; ">
#                                         No</th>
#                                     <th
#                                         style="text-align: center; padding: 8px; border-right: 4px solid black; background: #ddd; width: 60%;">
#                                         Item</th>
#                                     <th
#                                         style="text-align: center; padding: 8px; background: #ddd; width: 30%;">
#                                         Amount</th>
#                                 </tr>
#                             </thead>
#                             <tbody>
#                                 <tr style="border-bottom: 4px solid black;">
#                                     <td
#                                         style="padding: 8px; border-right: 4px solid black; text-align: center;">
#                                         1</td>
#                                     <td
#                                         style="padding: 8px; border-right: 4px solid black; text-align: center;">
#                                         margnita Pizza<br />
#                                          <span style="display: block;">3 x
#                                             200</span>
#                                          <span style="display: block;">HSN:
#                                             2300976</span>
#                                     </td>
#                                     <td
#                                         style="text-align: center; padding: 8px; background-color: #f5f5f5;">$
#                                         600</td>
#                                 </tr>
#                                 <tr style="border-bottom: 4px solid black;">
#                                     <td
#                                         style="padding: 8px; border-right: 4px solid black; text-align: center;">
#                                         2</td>
#                                     <td
#                                         style="padding: 8px; border-right: 4px solid black; text-align: center;">
#                                         Bacon Burger<br />
#                                          <span style="display: block;">5 x
#                                             150</span>
#                                     </td>
#                                     <td
#                                         style="text-align: center; padding: 8px; background-color: #f5f5f5;">$
#                                         750</td>
#                                 </tr>
#                                 <tr style="border-bottom: 4px solid black;">
#                                     <td
#                                         style="padding: 8px; border-right: 4px solid black; text-align: center;">
#                                         3</td>
#                                     <td
#                                         style="padding: 8px; border-right: 4px solid black; text-align: center;">
#                                         Apple Pie<br />
#                                          <span style="display: block;">3 x
#                                             80</span>
#                                          <span style="display: block;">HSN:
#                                             2300976</span>
#                                     </td>
#                                     <td
#                                         style="text-align: center; padding: 8px; background-color: #f5f5f5;">$
#                                         240</td>
#                                 </tr>
#                                 <tr style="border-bottom: 4px solid black;">
#                                     <td
#                                         style="padding: 8px; border-right: 4px solid black; text-align: center;">
#                                         4</td>
#                                     <td
#                                         style="padding: 8px; border-right: 4px solid black; text-align: center;">
#                                         Cheese Burger<br />
#                                          <span style="display: block;">5 x
#                                             150</span>
#                                          <span style="display: block;">HSN:
#                                             2300976</span>
#                                     </td>
#                                     <td
#                                         style="text-align: center; padding: 8px; background-color: #f5f5f5;">$
#                                         750</td>
#                                 </tr>
#                             </tbody>
#                             <tfoot>
#                                 <tr style="border-top: 2px solid black;">
#                                     <td colspan="2"
#                                         style="text-align: left; padding: 8px; font-weight: bold;">
#                                         Total Qty 16
#                                     </td>
#                                     <td
#                                         style="text-align: right; padding: 5px; font-weight: bold; background-color: #f5f5f5;">
#                                         <span> Sub Total $ 2340</span>
#                                     </td>
#                                 </tr>
#                                 <tr style="border-top: 2px solid black;">
#                                     <td colspan="3"
#                                         style="text-align: right; padding: 8px; background-color: #f5f5f5;">
#                                         Card $ 2340
#                                     </td>
#                                 </tr>
#                             </tfoot>
#                         </table>
#                         <br />
#                         <br />
#                         <hr />


#                         <table style="width: 100%; margin-bottom: 20px;">
#                             <thead>
#                                 <tr
#                                     style="border-top: 4px solid black; border-bottom: 4px solid black;">
#                                     <th
#                                         style="text-align: left; padding: 5px; background: #f0f0f0; border-bottom: 2px solid #ccc;">
#                                         Tax</th>
#                                     <th
#                                         style="text-align: right; padding: 5px; background: #f0f0f0; border-bottom: 2px solid #ccc;">
#                                         Amount</th>
#                                     <th
#                                         style="text-align: right; padding: 5px; background: #f0f0f0; border-bottom: 2px solid #ccc;">
#                                         Base</th>
#                                     <th
#                                         style="text-align: right; padding: 5px; background: #f0f0f0; border-bottom: 2px solid #ccc;">
#                                         Total</th>
#                                 </tr>
#                             </thead>
#                             <!-- <br /> -->
#                             <tbody>
#                                 <tr>
#                                     <td style="text-align: left; padding: 5px;">SGST 2.5%</td>
#                                     <td style="text-align: right; padding: 5px;">58.5 </td>
#                                     <td style="text-align: right; padding: 5px;">2281.5</td>
#                                     <td
#                                         style="text-align: right; padding: 5px; background-color: #f5f5f5;">
#                                         2340</td>
#                                 </tr>
#                                 <tr>
#                                     <td style="text-align: left; padding: 5px;">SGST 2.5%</td>
#                                     <td style="text-align: right; padding: 5px;">58.5 </td>
#                                     <td style="text-align: right; padding: 5px;">2281.5</td>
#                                     <td
#                                         style="text-align: right; padding: 5px; background-color: #f5f5f5;">
#                                         2340</td>
#                                 </tr>
#                             </tbody>
#                         </table>
#                     </t>

#                     <hr />
#                     <hr />
#                     <br />

#                     <!-- ✅ User Footer + System Footer -->
#                     <div class="text-center" style="text-align: center; margin-top: 10px;">
#                         <div style="text-align: center; margin-top: 20px;">
#                             <p style="margin: 0;">Odoo Point of Sale</p>
#                             <p style="margin: 0;">Order 0001-003-0004</p>
#                             <p style="margin: 0;">04/06/2024 08:30:24</p>
#                         </div>
#                         <br />
#                         <t t-out="footer_html" />
#                     </div>


#                 </div>
#             </div>
#         </t>
#     </t>
# """

    @api.depends('pos_config_id')
    def _compute_is_restaurant(self):
        for wizard in self:
            wizard.is_restaurant = wizard.pos_config_id.module_pos_restaurant if wizard.pos_config_id else False

    @api.depends('receipt_layout', 'receipt_header', 'receipt_footer', 'receipt_logo', 'is_restaurant')
    def _compute_preview_html(self):
        for wizard in self:
            context = {
                'layout_style': wizard.receipt_layout,
                'header_html': wizard.receipt_header or '',
                'footer_html': wizard.receipt_footer or '',
                'logo': wizard.receipt_logo or '',
                'is_restaurant': wizard.is_restaurant,
            }
            # wizard.preview_html = self.env['ir.qweb']._render_template_string(
            #     PREVIEW_TEMPLATE,
            #     context
            # )
            wizard.preview_html = self.env['ir.ui.view']._render_template(
                'pos_receipt_layout_customization.pos_receipt_preview_template_render',
                context
            )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        config_id = self.env.context.get('default_pos_config_id')
        config = self.env['pos.config'].browse(config_id) if config_id else self.env['pos.config']

        if config:
            res.update({
                'pos_config_id': config.id,
                'receipt_layout': config.receipt_layout,
                'receipt_header': config.receipt_header or '',
                'receipt_footer': config.receipt_footer or '',
                'receipt_logo': config.receipt_logo or '',
            })
        return res

    def action_save_receipt_layout(self):
        if self.pos_config_id:
            # Render the correct template
            template = {
                'light': 'pos_receipt_layout_customization.receipt_light_template',
                'lined': 'pos_receipt_layout_customization.receipt_lined_template',
                'boxed': 'pos_receipt_layout_customization.receipt_boxed_template',
            }.get(self.receipt_layout, 'pos_receipt_layout_customization.receipt_light_template')

            rendered_template = self.env['ir.ui.view']._render_template(
                template,
                {
                    'layout_style': self.receipt_layout,
                    'header_html': self.receipt_header or '',
                    'footer_html': self.receipt_footer or '',
                    'logo': self.receipt_logo or '',
                    'is_restaurant': self.is_restaurant,
                    # 'company': self.pos_config.company_id,
                    # 'orderlines': [
                    #     {'productName': 'Margherita Pizza', 'qty': 1, 'unitPrice': 200, 'price': 400},
                    #     {'productName': 'Cheese Burger', 'qty': 2, 'unitPrice': 150, 'price': 150},
                    #     {'productName': 'Cheese Burger', 'qty': 3, 'unitPrice': 450, 'price': 250},
                    # ]
                }
            )

            # ✅ Save everything including rendered HTML
            self.pos_config_id.write({
                'receipt_layout': self.receipt_layout,
                'receipt_header': self.receipt_header,
                'receipt_footer': self.receipt_footer,
                'receipt_logo': self.receipt_logo,
                'receipt_rendered_template': rendered_template,  # ✅ Store here
            })
        return {'type': 'ir.actions.act_window_close'}
