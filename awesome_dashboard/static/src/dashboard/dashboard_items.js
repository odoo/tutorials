import { NumberCard } from "./NumberCard/numberCard";
import { PieChartCard } from "./PieChartCard/PieChartCard";

export const items = [
  {
    id: "average_quantity",
    description: "Average amount of t-shirt",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
      title: "Average amount of t-shirt by order this month",
      value: data.average_quantity,
    })
  },

  {
    id: "average_time",
    description: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
    Component: NumberCard,
    size: 2,
    props: (data) => ({
      title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
      value: data.average_time,
    })
  },

  {
    id: "nb_new_orders",
    description: "Number of new orders this month",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
      title: "Number of new orders this month",
      value: data.nb_new_orders,
    })
  },

  {
    id: "total_amount",
    description: "Total amount--> of new orders this month",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
      title: "Total amount of new orders this month",
      value: data.total_amount,
    })
  },

  {
    id: "orders_by_size",
    description: "Shirt Orders by Size",
    Component: PieChartCard,
    size: 1,
    props: (data) => ({
      title: "Shirt Orders by Size",
      data: data.orders_by_size
    })
  }

];
