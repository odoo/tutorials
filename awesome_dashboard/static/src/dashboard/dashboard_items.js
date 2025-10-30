import {NumberCard} from "./number_card/number_card";
import {PieChartCard} from "./pie_chart_card/pie_chart_card";
import { registry } from "@web/core/registry";

const dashboardItems = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        // size and props are optionals
        size: 2,
        props: (data) =>  ({
                title: "Average amount of t-shirt by order this month",
                value: data.average_quantity
            })
    },
    {
        id: "average_time",
        description: "Average time for an order to go from new to sent or cancelled",
        Component: NumberCard,
        // size and props are optionals
        size: 2,
        props: (data) => ({
            title: "Average time for an order to go from new to sent or cancelled",
            value: data.average_time
        }),
    },
    {
        id: "nb_new_orders",
        description: "Number of new orders this month",
        Component: NumberCard,
        // size and props are optionals
        size: 1,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Number of cancelled this month",
        Component: NumberCard,
        // size and props are optionals
        size: 1,
        props: (data) => ({
            title: "Number of cancelled this month",
            value: data.nb_cancelled_orders
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
        id: "pie_chart",
        description: "!!! Pie !!!",
        Component: PieChartCard,
        // size and props are optionals
        size: 1,
        props: (data) => {
            return ({
                title: "Pie!",
                data: data.orders_by_size
            })
        },
    },
];

dashboardItems.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
})
