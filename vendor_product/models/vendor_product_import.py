import base64
import io
from openpyxl import load_workbook
from odoo import api, fields, models
from odoo.exceptions import UserError

class VendorProductImport(models.Model):
    _name = 'vendor.product.import'

    name = fields.Char(string="Name", default="New", readonly="1")
    vendor_id = fields.Many2one(comodel_name='res.partner', string="Vendor", required=True)
    vendor_template = fields.Many2one(comodel_name="vendor.product.template", string="Vendor Template Formate", domain="[('vendor_id', '=', vendor_id)]")
    file_to_process = fields.Binary(string="File to Process")
    date = fields.Datetime(string="Date", default=fields.Datetime.now)
    state = fields.Selection(
        selection=[
            ('pending', "Pending"),
            ('processed', "Processed"),
            ('error', "Error")
        ],
        string="State",
        default='pending'
    )

    @api.onchange('vendor_id')
    def _onchange_vendor_id(self):
        if self.vendor_id:
            template = self.env['vendor.product.template'].search([('vendor_id', '=', self.vendor_id.id)], limit=1)
            self.vendor_template = template.id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('vendor.product.import') or 'New'

        return super().create(vals_list)

    # Acction methods

    def action_reset_to_pending(self):
        self.state = 'pending'

    def action_manual_process(self):
        """Process the uploaded Excel file to update or create products based on product_unique_id."""
        if not self.file_to_process:
            self.state = 'error'
            raise UserError("Please upload an Excel file before processing.")

        if not self.vendor_template:
            self.state = 'error'
            raise UserError("No vendor template selected.")

        try:
            # 1: Read the Excel file
            file_content = base64.b64decode(self.file_to_process)
            file_stream = io.BytesIO(file_content)
            workbook = load_workbook(file_stream, data_only=True)
            sheet = workbook.worksheets[0]

            # 2: Get required field mappings from vendor template
            template_format_lines = self.vendor_template.template_formate_ids
            required_headers = template_format_lines.mapped('file_header')

            # 3: Validate headers
            header_tuple = tuple(cell.value for cell in sheet[1])
            missing_headers = set(required_headers) - set(header_tuple)
            if missing_headers:
                self.state = 'error'
                raise UserError(f"The uploaded file is missing required headers: {', '.join(missing_headers)}")

            # 4: Map Excel headers to Odoo fields
            field_mapping = {line.file_header: line.odoo_field.name for line in template_format_lines}

            # Ensure product_unique_id is part of the template format
            if 'product_unique_id' not in field_mapping.values():
                self.state = 'error'
                raise UserError("The field 'product_unique_id' must be in the template format.")

            # 5: Prepare data for product creation or update
            product_model = self.env['product.product']
            products_to_create = []
            products_to_update = []

            for row in sheet.iter_rows(min_row=2, values_only=True):
                product_data = {field_mapping[header]: row[header_tuple.index(header)] for header in field_mapping}

                existing_product = product_model.search([('product_unique_id', '=', product_data['product_unique_id'])], limit=1)

                if existing_product:
                    existing_product.write(product_data)
                    products_to_update.append(existing_product.id)
                else:
                    products_to_create.append(product_data)

            if products_to_create:
                product_model.create(products_to_create)

            self.state = 'processed'

            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': f'Successfully processed {len(products_to_create)} new product(s) and updated {len(products_to_update)} existing product(s).',
                    'type': 'rainbow_man',
                }
            }

        except Exception as e:
            self.state = 'error'
            raise UserError(f"An error occurred while processing the file: {str(e)}")