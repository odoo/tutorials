from odoo import api, fields, models
from odoo.exceptions import ValidationError


class LibraryBorrow(models.Model):
    _name = 'library.borrow'
    _description = "Library Borrows"

    book_id = fields.Many2one('library.book', required=True)
    member_id = fields.Many2one('library.member', required=True)
    borrow_date = fields.Date(default=lambda r: fields.Date.context_today(r))
    due_date = fields.Date(compute='_compute_due_date')
    return_date = fields.Date()
    state = fields.Selection(
        selection=[
            ('borrowed', "Borrowed"),
            ('returned', "Returned"),
            ('overdue', "Overdue")
        ],
        compute='_compute_state', store=True, readonly=False
    )
    fine_amount = fields.Integer(compute='_compute_fine', store=True)
    amount_paid = fields.Integer(readonly=True)

    account_move_ids = fields.One2many('account.move', 'library_borrow_id')

    @api.depends('borrow_date')
    def _compute_due_date(self):
        for rec in self:
            rec.due_date = fields.Date.add(rec.borrow_date, days=14)

    @api.depends('due_date', 'return_date')
    def _compute_state(self):
        for rec in self:
            if fields.Date.context_today(rec) > rec.due_date and not rec.return_date:
                rec.state = 'overdue'
            elif rec.return_date:
                rec.state = 'returned'
            else:
                rec.state = 'borrowed'

    @api.depends('due_date', 'state', 'return_date', 'amount_paid')
    def _compute_fine(self):
        for rec in self:
            due_days = 0
            if rec.state == 'returned':
                due_days = (rec.return_date - rec.due_date).days
            elif rec.state == 'overdue':
                due_days = (fields.Date.context_today(rec) - rec.due_date).days
            rec.fine_amount = (max(due_days, 0) * 5) - rec.amount_paid

    @api.constrains('member_id', 'book_id')
    def _check_availability(self):
        for rec in self:
            if not rec.member_id.is_eligible:
                raise ValidationError('Member is not eligible to borrow')
            elif rec.book_id.state == 'out_of_stock':
                raise ValidationError('Book is out of stock')
            duplicate = rec.search([
                ('member_id', '=', rec.member_id.id),
                ('book_id', '=', rec.book_id.id),
                ('state', '=', 'borrowed'),
                ('id', '!=', rec.id),
            ])
            if duplicate:
                raise ValidationError('Member Already Bought this book')

    def action_return(self):
        self.return_date = fields.Date.context_today(self)

    def action_waive_fine(self):
        return {
            'name': 'Pay Fine',
            'type': 'ir.actions.act_window',
            'res_model': 'library.waive.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_borrow_id': self.id,
            }

        }

    def action_open_invoice(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('library_borrow_id', '=', self.id)],
            'context': {'default_move_type': 'out_invoice', 'default_library_borrow_id': self.id}
        }
