/** @odoo-module **/

import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";
import { registry } from "@web/core/registry";

const items = [
  {
    id: "average_quantity",
    description: "Average amount of t-shirts",
    Component: NumberCard,
    props: (data) => ({
      header: "Average amount of t-shirts by order this month",
      value: data.average_quantity,
    }),
  },
  {
    id: "average_time",
    description: "Average time for an order",
    Component: NumberCard,
    props: (data) => ({
      header:
        "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
      value: data.average_time,
    }),
  },
  {
    id: "number_new_orders",
    description: "New orders this month",
    Component: NumberCard,
    props: (data) => ({
      header: "Number of new orders this month",
      value: data.nb_new_orders,
    }),
  },
  {
    id: "cancelled_orders",
    description: "Cancelled orders this month",
    Component: NumberCard,
    props: (data) => ({
      header: "Number of cancelled orders this month",
      value: data.nb_cancelled_orders,
    }),
  },
  {
    id: "amount_new_orders",
    description: "Total orders this month",
    Component: NumberCard,
    props: (data) => ({
      header: "Total amount of new orders this month",
      value: data.total_amount,
    }),
  },
  {
    id: "pie_chart_by_size",
    description: "Shirt orders by size",
    Component: PieChartCard,
    size: 2,
    props: (data) => ({
      header: "Shirt orders by size",
      data: data.orders_by_size,
    }),
  },
];

items.forEach((item) => {
  registry.category("awesome_dashboard").add(item.id, item);
});
