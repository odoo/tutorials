import { NumberCard } from "./NumberCard/number_card";
import { PieChartCard } from "./PieChartCard/pie_chart_card";
import { registry } from "@web/core/registry";

const dashboardItems = [
    {
        itemId: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
           title: "Average amount of t-shirt by order this month",
           value: data.average_quantity
        }),
     },
     {
        itemId: "new_orders_number",
        description: "Number of new orders",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
           title: "Average amount of t-shirt by order this month",
           value: data.nb_new_orders
        }),
     },
     {
        itemId: "cancelled_orders_number",
        description: "Number of cancelled orders",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
           title: "Number of cancelled orders this month",
           value: data.nb_cancelled_orders
        }),
     },
     {
      itemId: "average_time",
      description: "Average time for an order",
      Component: NumberCard,
      props: (data) => ({
          title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
          value: data.average_time,
      })
     },
     {
      itemId: "orders_by_size",
      description: "Order by Shirt Size",
      Component: PieChartCard,
      size: 3,
      props: (data) => ({
         title: "Number of orders by shirt size.",
         value: data.orders_by_size,
      }),
   },
]

dashboardItems.forEach((item) => {
   registry.category("awesome_dashboard").add(item.itemId, item);
})
