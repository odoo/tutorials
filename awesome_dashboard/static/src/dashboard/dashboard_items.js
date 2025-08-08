
import { NumberCard } from "./numberCard";
import { PieChartCard } from "./pieChartCard"
import { registry } from "@web/core/registry";

const dashboardAddItems = registry.category("awesome_dashboard")

dashboardAddItems.add("average_quantity", {
  id: "average_quantity",
  description: "Average amount of t-shirts",
  Component: NumberCard,
  size: 3,
  props: (data) => ({
    title: "Avg. T-shirts per order",
    value: data.average_quantity,
  }),
});

dashboardAddItems.add("average_time", {
  id: "average_time",
  description: "Average time for t-shirts",
  Component: NumberCard,
  size: 2,
  props: (data) => ({
    title: "Avg. Time per order",
    value: data.average_time,
  }),
});

dashboardAddItems.add("nb_new_orders", {
  id: "nb_new_orders",
  description: "New Orders",
  Component: NumberCard,
  size: 1,
  props: (data) => ({
    title: "New Orders",
    value: data.nb_new_orders,
  }),
});

dashboardAddItems.add("tot_amount", {
    id: "tot_amount",
    description: "Total Amount",
    Component: NumberCard,
    size: 3,
    props: (data) => ({
      title: "Total Amount",
      value: data.total_amount,
    }),
  });

dashboardAddItems.add("nb_cancel_orders", {
    id: "nb_cancel_orders",
    description: "Cancelled Orders",
    Component: NumberCard,
    size: 3,
    props: (data) => ({
      title: "Cancelled Orders",
      value: data.nb_cancelled_orders,
    }),
  });

  dashboardAddItems.add("orders_by_size", {
  id: "orders_by_size",
  description: "Orders by size",
  Component: PieChartCard,
  size: 3,
  props: (data) => ({
    title: "Orders by T-shirt size",
    data: data.orders_by_size,
  }),
});
