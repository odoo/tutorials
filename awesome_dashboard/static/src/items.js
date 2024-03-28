/** @odoo-module **/

import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";

const items = [
    {
        key: "average_quantity",
        description: _t("Average amount of t-shirt by order this month"),
    },
    {
        key: "average_time",
        description: _t("Average time for an order to go from 'new' to 'sent' or 'cancelled'"),
    },
    {
        key: "nb_cancelled_orders",
        description: _t("Number of cancelled orders this month"),
    },
    {
        key: "orders_by_size",
        description: _t("Orders by size"),
        presentation: "pie-chart",
    },
    {
        key: "total_amount",
        description: _t("Total amount of new orders this month"),
    },
];

for (const item of items) {
    registry.category("awesome_dashboard").add(item.key, item);
}
