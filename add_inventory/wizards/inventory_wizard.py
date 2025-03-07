from odoo import models, fields, api
from odoo.exceptions import ValidationError
import csv, base64, io

class InventoryImportWizard(models.TransientModel):
    _name = 'inventory.import.wizard'
    _description = 'Import Inventory Wizard'

    file = fields.Binary("Upload File", required=True)
    file_name = fields.Char("File Name")
    location_id = fields.Many2one(
        'stock.location',
        string="Destination Location",
        domain="[('usage', '=', 'internal')]"
    )
    operation = fields.Selection([
        ('add', 'Add Inventory'),
        ('remove', 'Remove Inventory'),
    ])
    storage_locations_enabled = fields.Boolean(
        compute='_compute_storage_location',
    )
    
    
    @api.model
    def default_get(self, fields_list):
        defaults = super(InventoryImportWizard, self).default_get(fields_list)
        
        storage_location = self.env['ir.config_parameter'].sudo().get_param('stock.storage_locations')
        defaults['storage_locations_enabled'] = bool(storage_location)

        if not defaults['storage_locations_enabled']:
            defaults['location_id'] = self.env.ref('stock.stock_location_stock').id  

        return defaults

                    
    
    def _get_or_create_product(self, product_data):
        """Retrieve or create a product based on product data dictionary."""
        product = self.env['product.product'].search([('name', '=', product_data['name'])], limit=1)
        if not product:
            uom_id = self.env['uom.uom'].search([('name', '=', product_data['uom'])], limit=1).id if product_data['uom'] else None
            product = self.env['product.product'].create({
                'name': product_data['name'],
                'is_storable': True,
                'type': 'consu',
                'tracking': 'serial' if product_data['quantity'] == 1 else 'lot' if product_data['serial_number'] else 'none',
                'company_id': self.env.company.id,
                'uom_id': uom_id,
                'uom_po_id': uom_id,
                'l10n_in_hsn_code': product_data['hsn_code'] if product_data['hsn_code'].isdigit() and len(product_data['hsn_code']) in (4, 6, 8) else '',
                'standard_price': product_data['cost']
            })
        return product

    def _get_or_create_lot(self, product_data, product):
        """Retrieve or create a lot/serial number for the given product."""
        if not product_data['serial_number']:
            return None
        lot = self.env['stock.lot'].search([('name', '=', product_data['serial_number']), ('product_id', '=', product.id)], limit=1)
        if not lot:
            lot = self.env['stock.lot'].create({'name': product_data['serial_number'], 'product_id': product.id, 'standard_price': product_data['cost']})
        return lot

    def _get_stock_quant(self, product_data, product, location, lot):
        """Retrieve or create stock quant based on operation type."""
        stock_quant = self.env['stock.quant'].search([
            ('product_id', '=', product.id),
            ('location_id', '=', location.id),
            ('lot_id', '=', lot.id if lot else None),
        ], limit=1)

        if self.operation == 'add':
            if stock_quant:
                stock_quant.quantity = product_data['quantity']
            else:
                stock_quant = self.env['stock.quant'].create({
                    'product_id': product.id,
                    'location_id': location.id,
                    'quantity': product_data['quantity'],
                    'lot_id': lot.id if lot else None,
                })

            self.env['stock.valuation.layer'].create({
                'product_id': product.id,
                'lot_id': lot.id,
                'value': product_data['quantity'] * product_data['cost'],
                'unit_cost': product_data['cost'],
                'quantity': product_data['quantity'],
                'company_id': self.env.company.ida
            })

        elif self.operation == 'remove':
            if not stock_quant or stock_quant.quantity < product_data['quantity']:
                return None
            stock_quant.quantity -= product_data['quantity']

        return stock_quant

    def _create_picking(self, picking_data):
        """Create a new stock picking."""
        return self.env['stock.picking'].create({
            'partner_id': self.env.user.company_id.partner_id.id,
            'location_id': picking_data['location_id'],
            'location_dest_id': picking_data['location_dest_id'],
            'picking_type_id': picking_data['picking_type'].id,
            'state': 'draft',
            'move_type': 'direct',
            'company_id': self.env.company.id
        })

    def _add_stock_move(self, move_data):
        """Add a stock move."""
        move = self.env['stock.move'].create({
            'name': move_data['product'].name,
            'picking_id': move_data['picking'].id,
            'product_id': move_data['product'].id,
            'product_uom_qty': move_data['quantity'],
            'location_id': move_data['location_id'],
            'location_dest_id': move_data['location_dest_id'],
            'product_uom': move_data['product'].uom_id.id,
        })

        self.env['stock.move.line'].create({
            'move_id': move.id,
            'product_id': move_data['product'].id,
            'quantity': move_data['quantity'],
            'location_id': move_data['location_id'],
            'location_dest_id': move_data['location_dest_id'],
            'lot_id': move_data['lot'].id if move_data['lot'] else None,
            'product_uom_id': move_data['product'].uom_id.id,
        })

    def action_import(self):
        """Import inventory from CSV file."""
        self.ensure_one()

        if not self.file_name.endswith('.csv'):
            raise ValidationError("Only CSV files are allowed for inventory imports.")

        file_content = base64.b64decode(self.file)
        file_stream = io.StringIO(file_content.decode("utf-8"))
        csv_reader = csv.reader(file_stream, delimiter=',')

        next(csv_reader, None)  
        company_id = self.env.company.id  

        for row in csv_reader:
            product_data = {
                'name': row[0],
                'serial_number': str(row[1]) if row[1] is not None else '',
                'quantity': float(row[2]),
                'uom': row[3],
                'hsn_code': row[4],
                'cost': float(row[5]) if row[5] and row[5].replace('.', '', 1).isdigit() else 0.0,
            }

            product = self._get_or_create_product(product_data)

            if (product.tracking in ('serial', 'lot') and not product_data['serial_number']) or (product.tracking == 'none' and product_data['serial_number']):
                continue

            if (product.tracking == 'serial' and product_data['quantity'] > 1) or (product.tracking == 'lot' and product_data['quantity'] <= 1):
                continue

            lot = self._get_or_create_lot(product_data, product)

            picking_data = {}
            if self.operation == 'add':
                picking_type = self.env['stock.picking.type'].search([('code', '=', 'incoming'), ('company_id', '=', company_id)], limit=1)
                picking_data.update({
                    'location_id': self.env.ref('stock.stock_location_suppliers').id,
                    'location_dest_id': self.location_id.id,
                })
            else:
                picking_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing'), ('company_id', '=', company_id)], limit=1)
                picking_data.update({
                    'location_id': self.location_id.id,
                    'location_dest_id': self.env.ref('stock.stock_location_customers').id,
                })

            if not picking_type:
                raise ValidationError("No suitable picking type found.")

            picking_data['picking_type'] = picking_type
            picking = self._create_picking(picking_data)

            if self.operation == 'add':
                stock_quant = self._get_stock_quant(product_data, product, self.location_id, lot)
                if not product.l10n_in_hsn_code and product_data['hsn_code'].isdigit() and len(product_data['hsn_code']) in (4, 6, 8):
                    product.l10n_in_hsn_code = product_data['hsn_code']
                if not product.standard_price:
                    product.standard_price = product_data['cost']
                if stock_quant:
                    self._add_stock_move({'picking': picking, 'product': product, 'quantity': product_data['quantity'], 'lot': lot, **picking_data})

            elif self.operation == 'remove':
                stock_quant = self._get_stock_quant(product_data, product, self.location_id, lot)
                if stock_quant:
                    self._add_stock_move({'picking': picking, 'product': product, 'quantity': product_data['quantity'], 'lot': lot, **picking_data})

            picking.action_confirm()
            picking.action_assign()
