import { NumberCard } from "./NumberCard";
import { PieChartCard } from "./charts/PieChartCard";
import { registry } from "@web/core/registry";

const items = [{
   id: "average_quantity",
   description: "Average amount of t-shirt by order this month",
   Component: NumberCard,
   // size and props are optionals
   size: 2,
   props: (data) => ({
      title: "Average amount of t-shirt by order this month",
      value: data.average_quantity
   }),
},

{
   id: "nb_new_orders",
   description: "Number of new orders this month",
   Component: NumberCard,
   // size and props are optionals
   size: 2,
   props: (data) => ({
      title: "Number of new orders this month",
      value: data.nb_new_orders
   }),
},


{
   id: "total_amount",
   description: "Total amount of new orders this month",
   Component: NumberCard,
   // size and props are optionals
   size: 2,
   props: (data) => ({
      title: "Total amount of new orders this month",
      value: data.total_amount
   }),
},


{
   id: "nb_cancelled_orders",
   description: "Number of cancelled orders this month",
   Component: NumberCard,
   // size and props are optionals
   size: 2,
   props: (data) => ({
      title: "Number of cancelled orders this month",
      value: data.nb_cancelled_orders
   }),
},

{
   id: "average_time",
   description: "Average time for an order to go from ‘new’ to ‘sent’ or ‘cancelled’",
   Component: NumberCard,
   // size and props are optionals
   size: 3,
   props: (data) => ({
      title: "Average time for an order to go from ‘new’ to ‘sent’ or ‘cancelled’",
      value: data.average_time
   }),
},

{
   id: "orders_by_size",
   description: "Shirt orders by size",
   Component: PieChartCard,
   // size and props are optionals
   size: 2,
   props: (data) => ({
      title: "Shirt orders by size",
      value: data.orders_by_size
   }),
}
]

registry.category("misc").add("awesome_dashboard.items", items);








