/** @odoo-module **/
import { registry } from "@web/core/registry";

import { NumberCard } from "./number_card";
import { PiechartCard } from "./piechart_card";

const items = [
    {
      id: "average_quantity",
      description: "Average amount of t-shirt by order this month",
      Component: NumberCard,
      size: 1,
      props: (data) => ({
        title: "Average amount of t-shirt by order this month",
        value: data.average_quantity,
      }),
    },
    {
      id: "average_time",
      description: "Average order processing time",
      Component: NumberCard,
      size: 2,
      props: (data) => ({
        title: "Avg. time from 'new' to 'sent' or 'cancelled'",
        value: data.average_time,
      }),
    },
    {
      id: "nb_new_orders",
      description: "Number of new orders",
      Component: NumberCard,
      size: 1,
      props: (data) => ({
        title: "Number of new orders this month",
        value: data.nb_new_orders,
      }),
    },
    {
      id: "nb_cancelled_orders",
      description: "Cancelled Orders",
      Component: NumberCard,
      size: 1,
      props: (data) => ({
        title: "Number of cancelled orders this month",
        value: data.nb_cancelled_orders,
      }),
    },
    {
      id: "total_amount",
      description: "Total Order Amount",
      Component: NumberCard,
      size: 1,
      props: (data) => ({
        title: "Total amount of new orders this month",
        value: data.total_amount,
      }),
    },
    {
      id: "orders_by_size",
      description: "Shirt Orders by Size",
      Component: PiechartCard,
      size: 2,
      props: (data) => ({
        title: "Shirt orders by size",
        data: data.orders_by_size,
      }),
    },
];

const dashboardRegistry = registry.category("awesome_dashboard");

items.forEach((item) => dashboardRegistry.add(item.id, item));
