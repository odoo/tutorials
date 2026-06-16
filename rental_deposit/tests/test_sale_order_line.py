from odoo.exceptions import UserError

from .common import RentalDepositCommon


class TestSaleOrderLine(RentalDepositCommon):

    # single product

    def test_deposit_line_created_on_rental_product_add(self):
        # adding single rental product to create one deposit line
        order = self._make_order()
        self._add_line(order, self.rental_product_a)

        deposit_lines = order.order_line.filtered(lambda l: l.is_deposit_line)
        self.assertEqual(len(deposit_lines), 1)
        self.assertEqual(deposit_lines.price_unit, 50.0)

    def test_deposit_line_linked_to_parent_rental_line(self):
        order = self._make_order()
        rental_line = self._add_line(order, self.rental_product_a)

        deposit_line = order.order_line.filtered(lambda l: l.is_deposit_line)
        self.assertEqual(deposit_line.parent_rental_line_id, rental_line)

    def test_no_deposit_line_for_non_deposit_product(self):
        order = self._make_order()
        self._add_line(order, self.rental_no_deposit)

        deposit_lines = order.order_line.filtered(lambda l: l.is_deposit_line)
        self.assertEqual(len(deposit_lines), 0)

    def test_deposit_line_qty_syncs_on_write(self):
        order = self._make_order()
        rental_line = self._add_line(order, self.rental_product_a, qty=1)

        rental_line.write({'product_uom_qty': 3})

        deposit_line = order.order_line.filtered(lambda l: l.is_deposit_line)
        self.assertEqual(deposit_line.product_uom_qty, 3)

    def test_deposit_line_deleted_with_rental_line(self):
        # deposit line should be removed via cascade
        order = self._make_order()
        rental_line = self._add_line(order, self.rental_product_a)

        rental_line.unlink()

        deposit_lines = order.order_line.filtered(lambda l: l.is_deposit_line)
        self.assertEqual(len(deposit_lines), 0)

    def test_direct_edit_of_deposit_line_raises_error(self):
        order = self._make_order()
        self._add_line(order, self.rental_product_a)

        deposit_line = order.order_line.filtered(lambda l: l.is_deposit_line)
        with self.assertRaises(UserError):
            deposit_line.write({'price_unit': 999})

    def test_direct_delete_of_deposit_line_raises_error(self):
        order = self._make_order()
        self._add_line(order, self.rental_product_a)

        deposit_line = order.order_line.filtered(lambda l: l.is_deposit_line)
        with self.assertRaises(UserError):
            deposit_line.unlink()

    def test_error_when_deposit_product_not_configured(self):
        self.env.company.deposit_product = False
        order = self._make_order()

        with self.assertRaises(UserError):
            self._add_line(order, self.rental_product_a)

        # reset so other tests aren't affected
        self.env.company.deposit_product = self.deposit_product

    # multiple products

    def test_multiple_deposit_lines_for_multiple_products(self):
        order = self._make_order()
        self._add_line(order, self.rental_product_a)
        self._add_line(order, self.rental_product_b)
        self._add_line(order, self.rental_product_c)

        deposit_lines = order.order_line.filtered(lambda l: l.is_deposit_line)
        self.assertEqual(len(deposit_lines), 3)

    def test_each_deposit_line_linked_to_correct_parent(self):
        order = self._make_order()
        line_a = self._add_line(order, self.rental_product_a)
        line_b = self._add_line(order, self.rental_product_b)

        deposit_a = order.order_line.filtered(
            lambda l: l.is_deposit_line and l.parent_rental_line_id == line_a
        )
        deposit_b = order.order_line.filtered(
            lambda l: l.is_deposit_line and l.parent_rental_line_id == line_b
        )
        self.assertEqual(len(deposit_a), 1)
        self.assertEqual(len(deposit_b), 1)

    def test_deposit_amounts_correct_for_multiple_products(self):
        order = self._make_order()
        self._add_line(order, self.rental_product_a)
        self._add_line(order, self.rental_product_b)
        self._add_line(order, self.rental_product_c)

        deposit_lines = order.order_line.filtered(lambda l: l.is_deposit_line)
        self.assertEqual(sorted(deposit_lines.mapped('price_unit')), [20.0, 30.0, 50.0])

    def test_mix_of_deposit_and_non_deposit_products(self):
        order = self._make_order()
        self._add_line(order, self.rental_product_a)
        self._add_line(order, self.rental_no_deposit)
        self._add_line(order, self.rental_product_b)

        deposit_lines = order.order_line.filtered(lambda l: l.is_deposit_line)
        self.assertEqual(len(deposit_lines), 2)

    def test_no_duplicate_deposit_lines_on_resave(self):
        # write() is called again when the order is saved — make sure
        # it doesn't create a second deposit line for the same rental line
        order = self._make_order()
        self._add_line(order, self.rental_product_a)

        order.write({'note': 'updated'})

        deposit_lines = order.order_line.filtered(lambda l: l.is_deposit_line)
        self.assertEqual(len(deposit_lines), 1)

    def test_qty_sync_per_product_independently(self):
        order = self._make_order()
        line_a = self._add_line(order, self.rental_product_a, qty=1)
        line_b = self._add_line(order, self.rental_product_b, qty=1)

        line_a.write({'product_uom_qty': 4})
        line_b.write({'product_uom_qty': 2})

        deposit_a = order.order_line.filtered(
            lambda l: l.is_deposit_line and l.parent_rental_line_id == line_a
        )
        deposit_b = order.order_line.filtered(
            lambda l: l.is_deposit_line and l.parent_rental_line_id == line_b
        )
        self.assertEqual(deposit_a.product_uom_qty, 4)
        self.assertEqual(deposit_b.product_uom_qty, 2)

    def test_qty_change_on_one_does_not_affect_other(self):
        order = self._make_order()
        line_a = self._add_line(order, self.rental_product_a, qty=1)
        line_b = self._add_line(order, self.rental_product_b, qty=1)

        line_a.write({'product_uom_qty': 5})

        deposit_b = order.order_line.filtered(
            lambda l: l.is_deposit_line and l.parent_rental_line_id == line_b
        )
        self.assertEqual(deposit_b.product_uom_qty, 1)

    def test_deleting_one_line_removes_only_its_deposit(self):
        order = self._make_order()
        line_a = self._add_line(order, self.rental_product_a)
        line_b = self._add_line(order, self.rental_product_b)

        line_a.unlink()

        deposit_lines = order.order_line.filtered(lambda l: l.is_deposit_line)
        self.assertEqual(len(deposit_lines), 1)
        self.assertEqual(deposit_lines.parent_rental_line_id, line_b)

    def test_deleting_all_lines_removes_all_deposits(self):
        order = self._make_order()
        line_a = self._add_line(order, self.rental_product_a)
        line_b = self._add_line(order, self.rental_product_b)
        line_c = self._add_line(order, self.rental_product_c)

        (line_a | line_b | line_c).unlink()

        deposit_lines = order.order_line.filtered(lambda l: l.is_deposit_line)
        self.assertEqual(len(deposit_lines), 0)

    def test_deleting_rental_line_keeps_non_deposit_line(self):
        # make sure cascade only removes the deposit line tied to the deleted
        # rental line, not unrelated lines on the same order
        order = self._make_order()
        line_a = self._add_line(order, self.rental_product_a)
        self._add_line(order, self.rental_no_deposit)

        line_a.unlink()

        remaining = order.order_line.filtered(
            lambda l: l.product_id == self.rental_no_deposit
        )
        self.assertEqual(len(remaining), 1)
