{
    'name': 'Sale Discount Recompute',
    'version': '1.0',
    'depends': ['sale_management'],
    'author': 'Jay Chauhan',
    'category': 'Sales',
    'summary': 'Automatic Global Discount Recalculation on Sale Orders',
    'description': '''
        This feature ensures proper handling of a global discount on Sale Orders.

        - When order lines are added, removed, or updated, the discount line is automatically recalculated to reflect the new subtotal.
        - If all order lines are removed, the discount line is also removed.
        - Prevents stale discount amounts from remaining when order content changes.
    ''',
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3'
}
