import { NumberCard } from "./dashboard/cards/number_card/number_card";
import { PieChartCard } from "./dashboard/cards/pie_chart_card/pie_chart_card";

export const itemsList = [
    {
       id: "nb_new_orders",
       description: "Number of new orders this month",
       Component: NumberCard,
       props: (data) => ({
          title: "Number of new orders this month",
          value: data.nb_new_orders
       }),
    },
    {
       id: "total_amount",
       description: "Total amount of new orders this month",
       Component: NumberCard,
       props: (data) => ({
          title: "Total amount of new orders this month",
          value: data.total_amount
       }),
    },
    {
       id: "average_quantity",
       description: "Average amount of t-shirt",
       Component: NumberCard,
       size: 2,
       props: (data) => ({
          title: "Average amount of t-shirt by order this month",
          value: data.average_quantity
       }),
    },
    {
       id: "nb_cancelled_orders",
       description: "Number of cancelled orders this month",
       Component: NumberCard,
       props: (data) => ({
          title: "Number of cancelled orders this month",
          value: data.nb_cancelled_orders
       }),
    },
    {
       id: "average_time",
       description: "Average time from 'new' to 'sent' or 'cancelled'",
       Component: NumberCard,
       size: 2,
       props: (data) => ({
          title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
          value: data.average_time
       }),
    },
    {
       id: "orders_by_size_chart",
       description: "Beautiful  C̶A̶M̶E̶M̶B̶E̶R̶T̶ pie chart (to faire plaisir à Serge ;D ) 🥰",
       Component: PieChartCard,
       size: 2,
       props: (data) => ({
          title: "A beautiful graph",
          values: data.orders_by_size
       }),
    }
 ];
 