import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";

export let items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        // size and props are optionals
        size: 3,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity
        }),
    },
    {
        id: "average_time",
        description: "Average time for an order",
        Component: NumberCard,
        // size and props are optionals
        props: (data) => ({
            title: "Average time for an order to go from new to sent or canceled",
            value: data.average_time
        }),
    },
    {
        id: "nb_new_orders",
        description: "New orders this month",
        Component: NumberCard,
        // size and props are optionals
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders
        }),
    }, {
        id: "nb_cancelled_orders",
        description: "Canceled orders this month",
        Component: NumberCard,
        // size and props are optionals
        props: (data) => ({
            title: "Number of canceled orders this month",
            value: data.nb_cancelled_orders
        }),
    },
    {
        id: "total_amount",
        description: "Smount of orders this month",
        Component: NumberCard,
        // size and props are optionals
        props: (data) => ({
            title: "Total amount of orders this month",
            value: data.total_amount
        }),
    },
    {
        id: "orders_by_size",
        description: "Shirt orders by size",
        Component: PieChartCard,
        // size and props are optionals
        props: (data) => ({
            title: "Shirt orders by size",
            values: data.orders_by_size
        }),
    },

];
