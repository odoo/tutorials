import random

from odoo import http


class AwesomeDashboard(http.Controller):
    @http.route("/awesome_dashboard/statistics", type="json", auth="user")
    def get_statistics(self):
        """Return order statistics including averages, counts, and amounts"""
        return {
            "average_quantity": random.randint(4, 12),
            "average_time": random.randint(4, 123),
            "nb_cancelled_orders": random.randint(0, 50),
            "nb_new_orders": random.randint(10, 200),
            "orders_by_size": {
                "m": random.randint(0, 150),
                "s": random.randint(0, 150),
                "xl": random.randint(0, 150),
            },
            "total_amount": random.randint(100, 1000),
        }
