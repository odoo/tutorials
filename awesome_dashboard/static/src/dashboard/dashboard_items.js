import { NumberCard } from "./components/cards/number_card";
import { PieChartCard } from "./components/cards/pie_chart_card";
import { registry } from "@web/core/registry";

const items = [
  {
    id: "average_quantity",
    description: "Average amount of t-shirt",
    Component: NumberCard,
    size: 2,
    props: (data) => ({
      title: "Average amount of t-shirt by order this month",
      value: data.average_quantity,
    }),
  },
  {
    id: "average_time",
    description: "Average processing time",
    Component: NumberCard,
    size: 3,
    props: (data) => ({
      title:
        "Average time for an order to go from ‘new’ to ‘sent’ or ‘cancelled’",
      value: data.average_time,
    }),
  },
  {
    id: "nb_new_orders",
    description: "New Orders This Month",
    Component: NumberCard,
    size: 1.5,
    props: (data) => ({
      title: "Number of new orders this month",
      value: data.nb_new_orders,
    }),
  },
  {
    id: "nb_cancelled_orders",
    description: "Cancelled Orders This Month",
    Component: NumberCard,
    size: 1.5,
    props: (data) => ({
      title: "Number of cancelled orders this month",
      value: data.nb_cancelled_orders,
    }),
  },
  {
    id: "total_amount",
    description: "Total Sales",
    Component: NumberCard,
    size: 1.5,
    props: (data) => ({
      title: "Total amount of new orders this month",
      value: data.total_amount,
    }),
  },
  {
    id: "orders_by_size",
    description: "T-shirt Orders by Size",
    Component: PieChartCard,
    size: 2,
    props: (data) => ({
      title: "T-shirt orders by size",
      data: data.orders_by_size,
    }),
  },
];

items.forEach((item) => {
  registry.category("awesome_dashboard").add(item.id, item);
});
