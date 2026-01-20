/** @odoo-module **/

import { NumberCard } from "./NumberCard/numbercard";
import { PieCard } from "./PieCard/piecard";
import { registry } from "@web/core/registry";

const dashboardItems = registry.category("awesome_dashboard");

dashboardItems.add("average_quantity", {
  id: "average_quantity",
  description: "Average amount of t-shirts",
  Component: NumberCard,
  size: 3,
  props: (data) => ({
    title: "Avg. T-shirts per order",
    value: data.average_quantity,
  }),
});

dashboardItems.add("average_time", {
  id: "average_time",
  description: "Average time for t-shirts",
  Component: NumberCard,
  size: 2,
  props: (data) => ({
    title: "Avg. Time per order",
    value: data.average_time,
  }),
});
dashboardItems.add("nb_new_orders", {
  id: "nb_new_orders",
  description: "New Orders",
  Component: NumberCard,
  size: 1,
  props: (data) => ({
    title: "New Orders",
    value: data.nb_new_orders,
  }),
});
dashboardItems.add("total_amount", {
    id: "total_amount",
    description: "Total Amount",
    Component: NumberCard,
    size: 3,
    props: (data) => ({
      title: "Total Amount",
      value: data.total_amount,
    }),
  });
dashboardItems.add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: "Cancelled Orders",
    Component: NumberCard,
    size: 3,
    props: (data) => ({
      title: "Cancelled Orders",
      value: data.nb_cancelled_orders,
    }),
  });
  
dashboardItems.add("orders_by_size", {
  id: "orders_by_size",
  description: "Orders by size",
  Component: PieCard,
  size: 1,
  props: (data) => ({
    title: "Orders by T-shirt size",
    data: data,
  }),
});
// export const items = [
//   {
//     id: "avg_quantity",
//     description: "Average amount of t-shirts",
//     Component: NumberCard,
//     size: 3,
//     props: (data) => ({
//       title: "Avg. T-shirts per order",
//       value: data.average_quantity,
//     }),
//   },
//   {
//     id: "avg_time",
//     description: "Average amount of t-shirts",
//     Component: NumberCard,
//     size: 2,
//     props: (data) => ({
//       title: "Avg. Time per order",
//       value: data.average_time,
//     }),
//   },
//   {
//     id: "nb_new_orders",
//     description: "Average amount of t-shirts",
//     Component: NumberCard,
//     size: 1,
//     props: (data) => ({
//       title: "Avg. T-shirts per order",
//       value: data.average_quantity,
//     }),
//   },
//   {
//     id: "order_distribution",
//     description: "Orders by size",
//     Component: PieCard,
//     size: 1,
//     props: (data) => ({
//       title: "Orders by T-shirt size",
//       data: data,
//     }),
//   },
// ];
