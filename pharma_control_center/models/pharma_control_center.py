from odoo import models, fields, api
from datetime import date, timedelta


class PharmaControlCenter(models.Model):
    _name = "pharma.control.center"
    _description = "Pharma Control Center"
    _rec_name = "user_id"

    # --- User profile (stored, writable) ---
    user_id = fields.Many2one('res.users', string="User", required=True, default=lambda self: self.env.user)
    avatar = fields.Binary(string="Profile Picture", attachment=True)
    avatar_filename = fields.Char(string="Avatar Filename")

    # Editable profile fields (stored locally)
    display_name = fields.Char(string="Full Name", required=True)
    email = fields.Char(string="Email", required=True)
    phone = fields.Char(string="Phone")



    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            rec._sync_user_profile()
        return records

    def write(self, vals):
        res = super().write(vals)
        if any(field in vals for field in ['display_name', 'email', 'phone']):
            self._sync_user_profile()
        return res

    def _sync_user_profile(self):
        """Sync local fields to res.users and res.partner."""
        for rec in self:
            user = rec.user_id
            partner = user.partner_id
            if partner.name != rec.display_name:
                partner.write({'name': rec.display_name})
                user.write({'name': rec.display_name})
            if partner.email != rec.email:
                partner.write({'email': rec.email})
                user.write({'email': rec.email})
            if partner.phone != rec.phone:
                partner.write({'phone': rec.phone})

    # --- Medicine statistics (unchanged) ---
    total_medicines = fields.Integer(string="Total Medicines", compute="_compute_statistics", store=False)
    total_stock_quantity = fields.Integer(string="Total Stock Quantity", compute="_compute_statistics", store=False)
    stock_value = fields.Float(string="Stock Value", compute="_compute_statistics", store=False)
    out_of_stock_count = fields.Integer(string="Out of Stock", compute="_compute_statistics", store=False)
    low_stock_count = fields.Integer(string="Low Stock (< 10)", compute="_compute_statistics", store=False)
    expiring_soon_count = fields.Integer(string="Expiring ≤30 Days", compute="_compute_statistics", store=False)
    expired_count = fields.Integer(string="Expired", compute="_compute_statistics", store=False)

    # --- Patient statistics (unchanged) ---
    total_patients = fields.Integer(string="Total Patients", compute="_compute_statistics", store=False)
    my_patients = fields.Integer(string="My Patients", compute="_compute_statistics", store=False)
    patient_ids = fields.One2many('pharmacy.patient', string="Patients", compute='_compute_patient_ids', readonly=True)

    # --- Today's orders summary (unchanged) ---
    today_order_total_qty = fields.Float(string="Total Quantity Today", compute="_compute_today_orders_summary",
                                         store=False)
    today_order_total_amount = fields.Float(string="Total Sales Today", compute="_compute_today_orders_summary",
                                            store=False)

    # -------------------------------------------------------------------------
    # Compute methods (unchanged)
    # -------------------------------------------------------------------------
    @api.depends()
    def _compute_statistics(self):
        Medicine = self.env['pharmacy.medicine']
        Patient = self.env['pharmacy.patient']
        today = date.today()
        thirty_days_later = today + timedelta(days=30)

        for rec in self:
            all_meds = Medicine.search([])
            rec.total_medicines = len(all_meds)
            rec.total_stock_quantity = sum(med.quantity for med in all_meds)
            rec.stock_value = sum(med.quantity * med.price for med in all_meds)
            rec.out_of_stock_count = sum(1 for med in all_meds if med.quantity == 0)
            rec.low_stock_count = sum(1 for med in all_meds if 0 < med.quantity < 10)
            rec.expiring_soon_count = sum(
                1 for med in all_meds
                if med.expiry_date and med.expiry_date <= thirty_days_later and med.expiry_date > today
            )
            rec.expired_count = sum(1 for med in all_meds if med.expiry_date and med.expiry_date < today)

            if Patient:
                rec.total_patients = Patient.search_count([])
                if self.env.user.has_group('pharma_control_center.group_pharmacy_doctor'):
                    rec.my_patients = Patient.search_count([('doctor_id', '=', self.env.user.id)])
                else:
                    rec.my_patients = 0
            else:
                rec.total_patients = 0
                rec.my_patients = 0

    @api.depends()
    def _compute_patient_ids(self):
        Patient = self.env['pharmacy.patient']
        for rec in self:
            if self.env.user.has_group('pharma_control_center.group_pharmacy_doctor'):
                rec.patient_ids = Patient.search([('doctor_id', '=', self.env.user.id)])
            elif self.env.user.has_group('pharma_control_center.group_pharmacy_manager'):
                rec.patient_ids = Patient.search([])
            else:
                rec.patient_ids = False

    @api.depends()
    def _compute_today_orders_summary(self):
        today = fields.Date.today()
        tomorrow = today + timedelta(days=1)
        domain = [
            ('order_id.date_order', '>=', today),
            ('order_id.date_order', '<', tomorrow),
            ('order_id.state', 'not in', ['cancel'])
        ]
        if not self.env.user.has_group('pharma_control_center.group_pharmacy_manager'):
            domain.append(('create_uid', '=', self.env.user.id))
        lines = self.env['sale.order.line'].search(domain)
        self.today_order_total_qty = sum(lines.mapped('product_uom_qty'))
        self.today_order_total_amount = sum(lines.mapped('price_subtotal'))

    # -------------------------------------------------------------------------
    # Actions (unchanged)
    # -------------------------------------------------------------------------
    def action_view_today_orders(self):
        today = fields.Date.today()
        tomorrow = today + timedelta(days=1)
        domain = [
            ('order_id.date_order', '>=', today),
            ('order_id.date_order', '<', tomorrow),
            ('order_id.state', 'not in', ['cancel'])
        ]
        if not self.env.user.has_group('pharma_control_center.group_pharmacy_manager'):
            domain.append(('create_uid', '=', self.env.user.id))

        view = self.env.ref('pharma_control_center.view_sale_order_line_today_list', raise_if_not_found=False)
        view_id = view.id if view else False
        return {
            'type': 'ir.actions.act_window',
            'name': "Today's Orders",
            'res_model': 'sale.order.line',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': domain,
            'views': [(view_id, 'list')] if view_id else [(False, 'list')],
        }

    @api.model
    def _ensure_one_per_user(self):
        user = self.env.user
        record = self.search([('user_id', '=', user.id)], limit=1)
        if not record:
            record = self.create(
                {'user_id': user.id, 'display_name': user.name, 'email': user.email, 'phone': user.phone})
        return record.id
