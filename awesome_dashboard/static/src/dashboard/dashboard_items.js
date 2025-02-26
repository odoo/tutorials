// imports
import { NumberCard } from "@awesome_dashboard/dashboard/number_card/number_card";
import { PieChartCard } from "@awesome_dashboard/dashboard/pie_chart_card/pie_chart_card";
import { registry } from "@web/core/registry"

// array of dashboard items, each representing a different statistics
const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity, // Fetching data 
        })
    },
    {
        id: "average_time",
        description: "Average time for an order",
        Component: NumberCard,
        props: (data) => ({
            title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
            value: data.average_time,
        })
    },
    {
        id: "number_new_orders",
        description: "New orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders,
        })
    },
    {
        id: "cancelled_orders",
        description: "Cancelled orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders,
        })
    },
    {
        id: "amount_new_orders",
        description: "amount orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.total_amount,
        })
    },
    {
        id: "pie_chart",
        description: "Shirt orders by size",
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: "Shirt orders by size",
            values: data.orders_by_size,
        })
    }
]

// registering each dashboard item in the awesome_dashboard category
items.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
})
