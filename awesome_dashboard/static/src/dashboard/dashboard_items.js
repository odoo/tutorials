/** @odoo-module **/

import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";

const items = [
    {
        id: "average_quantity",
        description: _t("Average amount of t-shirt"),
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
            title: _t("Average amount of t-shirt by order this month"),
            value: data.average_quantity,
        }),
    },
    {
        id: "average_time",
        description: _t("Average time for an order"),
        Component: NumberCard,
        size: 1.75,
        props: (data) => ({
            title: _t("Average time for an order to go from 'new' to 'sent' or 'cancelled'"),
            value: data.average_time,
        }),
    },
    {
        id: "number_new_orders",
        description: _t("New orders this month"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Number of new orders this month"),
            value: data.nb_new_orders,
        }),
    },
    {
        id: "cancelled_orders",
        description: _t("Cancelled orders this month"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Number of cancelled orders this month"),
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "amount_new_orders",
        description: _t("amount orders this month"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Total amount of new orders this month"),
            value: data.total_amount,
        }),
    },
    {
        id: "pie_chart",
        description: _t("Shirt orders by size"),
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: _t("Shirt orders by size"),
            values: data.orders_by_size,
        }),
    },
];

const HIDDEN_ITEM_IDS_STORAGE_KEY = "awesome_dashboard.hiddenItemIds";

export function loadHiddenItemIds() {
    return localStorage.getItem(HIDDEN_ITEM_IDS_STORAGE_KEY)?.split(",") || [];
}

export function setHiddenItemIds(disablesIds) {
    localStorage.setItem(HIDDEN_ITEM_IDS_STORAGE_KEY, disablesIds.join(","));
}

function loadItems() {
    const hiddenIds = loadHiddenItemIds();
    items.forEach((i) => {
        i.show = !hiddenIds.includes(i.id);
        registry.category("dashboard_item_registry").add(i.id, i);
    });
}

loadItems();
