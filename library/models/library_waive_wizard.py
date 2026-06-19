from odoo import api, Command, fields, models
from odoo.exceptions import ValidationError


class LibraryWaiveWizard(models.TransientModel):
    _name = 'library.waive.wizard'
    _description = "Fine Waiving Wizard"

    total_fine = fields.Integer(compute='_compute_fine_amount', readonly=True)
    paid_amount = fields.Integer()
    remaining_amount = fields.Integer(compute='_compute_remaining_amount', readonly=True)
    borrow_id = fields.Many2one('library.borrow', readonly=True)

    @api.depends('borrow_id')
    def _compute_fine_amount(self):
        for rec in self:
            rec.total_fine = rec.borrow_id.fine_amount

    @api.depends('total_fine', 'paid_amount')
    def _compute_remaining_amount(self):
        for rec in self:
            rec.remaining_amount = rec.total_fine - rec.paid_amount

    @api.constrains('paid_amount')
    def _check_paid_amount(self):
        for rec in self:
            if rec.paid_amount > rec.total_fine:
                raise ValidationError("Cannot pay more than fine amount")

    def action_pay(self):
        self.borrow_id.amount_paid += self.paid_amount
        for rec in self:
            self.env['account.move'].create({
                'move_type': 'out_invoice',
                'member_id': rec.borrow_id.member_id.id,
                'library_borrow_id': rec.borrow_id.id,
                'invoice_line_ids': [
                    Command.create({'name': "%s Fine" % rec.borrow_id.book_id.name, 'quantity': 1, 'price_unit': rec.paid_amount}),
                ]
            })
        return {'type': 'ir.actions.act_window_close'}
