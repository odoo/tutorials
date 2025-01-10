from odoo import models,fields, Command
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_emi = fields.Boolean()
    next_installment_date = fields.Date()
    installment_invoice_ids = fields.One2many('account.move', 'sale_order_id')

    def _cron_recurring_create_installment_invoice(self):
        today = fields.Date.context_today(self)

        #for regular installments
        sale_orders = self.search([('is_emi', '=', True), ('next_installment_date', '<=', today)])

        # Fetch the installment product
        installment_product = self.env.ref('installments.product_product_installment', False)
        
        # fetch configuration values from settings
        config = self.env['ir.config_parameter'].sudo()
        down_payment_percentage = float(config.get_param('installment.down_payment_percentage', 0.0))
        annual_rate_percentage = float(config.get_param('installment.annual_rate_percentage', 0.0))
        max_duration = float(config.get_param('installment.max_duration', 1))
        admin_expenses_percentage = float(config.get_param('installment.admin_expenses_percentage', 0.0))
        delay_penalty_process = float(config.get_param('installment.delay_penalty_days', 0.0))
        delay_penalty_percentage = float(config.get_param('installment.delay_penalty_percentage', 0.0))

        for sale_order in sale_orders:
            # Calculate financial values
            down_payment = (down_payment_percentage / 100) * sale_order.amount_total
            remaining_amount = sale_order.amount_total - down_payment
            admin_expenses = (admin_expenses_percentage / 100) * remaining_amount
            remaining_amount += admin_expenses
            interest = (remaining_amount * annual_rate_percentage * max_duration) / 100
            total_with_interest = remaining_amount + interest
            monthly_installment_count = max_duration * 12
            monthly_installment_amount = total_with_interest / monthly_installment_count if monthly_installment_count else 0.0

            # Check if there are already 24 invoices
            if len(sale_order.installment_invoice_ids) >= monthly_installment_count:
                sale_order.next_installment_date = False
                continue
         
            # Create the installment invoice
            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': sale_order.partner_id.id,
                'invoice_date': today,
                'invoice_date_due': today + timedelta(days=30),
                'invoice_line_ids': [
                    Command.create({
                        'product_id': installment_product.id,
                        'quantity': 1,
                        'price_unit': monthly_installment_amount,
                        'tax_ids': None,
                    })
                ],
                'sale_order_id': sale_order.id,
            }
            invoice = self.env['account.move'].create(invoice_vals)
            sale_order.installment_invoice_ids = [Command.link(invoice.id)]
            # Update the next installment date
            sale_order.next_installment_date = sale_order.next_installment_date + relativedelta(months=1) if sale_order.next_installment_date else None

        #For penalty invoices
        delay_penalty_date = today - timedelta(days=delay_penalty_process)

        # Fetch the penalty product
        penalty_product = self.env.ref('installments.product_product_penalty', False)
        invoices = self.env["account.move"].search([
            ("move_type", "=", "out_invoice"),
            ("state", "=", "draft"),
            ('sale_order_id', "!=", False),
            ("is_penalty_applied", "=", False),
            ("invoice_date", "<=", delay_penalty_date),
        ])
        for invoice in invoices:
            #calculate penalty amount
            penalty_amount=(delay_penalty_percentage/100)*invoice.amount_total
            # Create the penalty invoice
            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': invoice.partner_id.id,
                'invoice_date': today,
                'invoice_date_due': today + timedelta(days=30),
                'invoice_line_ids': [
                    Command.create({
                        'product_id': penalty_product.id,
                        'quantity': 1,
                        'price_unit': penalty_amount,
                        'tax_ids': None,
                    })
                ],
                'is_penalty_applied': True,
            }
            penalty_invoice = self.env['account.move'].create(invoice_vals)

            invoice.write(
                        {
                            'is_penalty_applied': True,
                            'penalty_invoice_id':penalty_invoice.id
                        })

    def action_open_installment_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Installment Information',
            'res_model': 'installment.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('installments.add_emi_wizard_form_view').id,
            'target': 'new',
        } 

    def action_open_installment_invoices(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Installment invoices',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('sale_order_id', '=', self.id)], 
            'target': 'current',
        }

    def action_document_upload(self):
        installment_folder = self.env["documents.document"].search(
            [("name", "=", "Sales - Installment")], limit=1
        )

        if not installment_folder:
            installment_folder = self.env["documents.document"].create(
                {
                    "name": "Sales - Installment",
                    "folder_id": None,
                }
            )

        subfolder = self.env["documents.document"].search([("name", "=", self.name)])
        if not subfolder:
            subfolder = self.env["documents.document"].create(
                {
                    "name": self.name,
                    'type': 'folder',
                    "folder_id": installment_folder.id,
                }
            )
        if not subfolder:
            raise ValidationError(
                "Failed to create or find the corresponding subfolder."
            )

        # Configuration parameters for required documents
        settings = self.env["ir.config_parameter"]
        documents_to_upload = {
            "NID": settings.get_param("installment.nid_required") == "True",
            "Salary Components": settings.get_param("installment.salary_components_required") == "True",
            "Bank Statement": settings.get_param("installment.bank_statement_required") == "True",
            "Bank Rate Letter": settings.get_param("installment.bank_rate_letter_required") == "True",
            "Rental Contract": settings.get_param("installment.rental_contract_required") == "True",
            "Ownership Contract": settings.get_param("installment.ownership_contract_required") == "True",
        }
        required_documents_count = sum(1 for is_required in documents_to_upload.values() if is_required)
        # Create document requests for required documents
        for doc_name, is_required in documents_to_upload.items():
            if is_required:
                existing_documents = self.env["documents.document"].search(
                    [
                        ("folder_id", "=", subfolder.id),
                    ],
                )

                # prevent request creation if document for the request is already uploaded
                if len(existing_documents)<required_documents_count:
                    existing_document = self.env["documents.document"].search(
                    [
                        ("name", "=", doc_name),
                        ("folder_id", "=", subfolder.id),
                    ],
                    limit=1)

                    # Create the request only if it does not already exist
                    if not existing_document:
                        self.env["documents.document"].create(
                            {
                                "name": doc_name,
                                "folder_id": subfolder.id,
                            })
        return {
            "type": "ir.actions.act_window",
            "name": "Documents",
            "res_model": "documents.document",
            "view_mode": "kanban,list,form",
            "domain": [("folder_id", "=", subfolder.id)],
            "context": {"searchpanel_default_folder_id": subfolder.id},
        }
    
    #Override default confirm action to prevent user from confirming invoice without uploading required documents
    def _action_confirm(self):
         # Configuration parameters for required documents
        settings = self.env["ir.config_parameter"]
        documents_to_upload = {
            "NID": settings.get_param("installment.nid_required") == "True",
            "Salary Components": settings.get_param("installment.salary_components_required") == "True",
            "Bank Statement": settings.get_param("installment.bank_statement_required") == "True",
            "Bank Rate Letter": settings.get_param("installment.bank_rate_letter_required") == "True",
            "Rental Contract": settings.get_param("installment.rental_contract_required") == "True",
            "Ownership Contract": settings.get_param("installment.ownership_contract_required") == "True",
        }
        required_documents_count = sum(1 for is_required in documents_to_upload.values() if is_required)

        existing_documents = self.env["documents.document"].search(
                    [
                        ("folder_id", "=", self.name),
                        ("attachment_type","=","binary")
                    ],
                )

        if len(existing_documents)<required_documents_count:
                raise ValidationError("Please upload required documents to confirm the sales order.")
        return super()._action_confirm()
