import { Number } from "./component/number";
import { PieChart } from "./component/pie_chart";
import { registry } from "@web/core/registry";

const items = [
  {
    id: "average_quality",
    description: "Average amount of t-shirts",
    Component: Number,
    props: (data) => ({
      title: "Average amount of t-shirts by order this month",
      value: data.average_quantity
    })
  },
  {
    id: "average_time",
    description: "Average order time",
    Component: Number,
    props: (data) => ({
      title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
      value: data.average_time
    })
  },
  {
    id: "new_orders",
    description: "New orders",
    Component: Number,
    props: (data) => ({
      title: "Number of new orders this month",
      value: data.nb_new_orders
    })
  },
  {
    id: "cancelled_orders",
    description: "Cancelled orders",
    Component: Number,
    props: (data) => ({
      title: "Number of cancelled orders this month",
      value: data.nb_cancelled_orders
    })
  },
  {
    id: "total_amount",
    description: "New orders total",
    Component: Number,
    props: (data) => ({
      title: "Total amount of new orders",
      value: data.total_amount
    })
  },
  {
    id: "pie",
    description: "Pie",
    Component: PieChart,
    size: 2,
    props: (data) => ({
      title: "Shirt orders by size",
      data: {
        labels: Object.keys(data.orders_by_size),
        datasets: [{
          data: Object.values(data.orders_by_size),
        }],
      }
    })
  },
]

items.forEach(i => registry.category("awesome_dashboard").add(i.id, i))
