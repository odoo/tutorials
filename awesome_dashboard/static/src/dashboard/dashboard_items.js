import { NumberCard } from "./numberCard/numberCard";
import { PieChartCard } from "./pieChartCard/pieChartCard";
import { registry } from "@web/core/registry";


export const items = [{
    id: "average_quantity",
    Component: NumberCard,
    size: 1.2,
    props: (data) => ({
        title: "Average amount of t-shirt by order this month",
        value: data.average_quantity
    })
}, {
    id: "average_time",
    Component: NumberCard,
    size: 2,
    props: (data) => ({
        title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
        value: data.average_time
    })
}, {
    id: "nb_new_orders",
    Component: NumberCard,
    props: (data) => ({
        title: "Number of new orders this month",
        value: data.nb_new_orders
    })
}, {
    id: "nb_cancelled_orders",
    Component: NumberCard,
    props: (data) => ({
        title: "Number of cancelled orders this month",
        value: data.nb_cancelled_orders
    })
}, {
    id: "total_amount",
    Component: NumberCard,
    props: (data) => ({
        title: "Total amount of new orders this month",
        value: data.total_amount
    })
}, {
    id: "orders_by_size",
    Component: PieChartCard,
    size: 2.5,
    props: (data) => ({
        title: "Shirt orders by size",
        data: data.orders_by_size ? Object.entries(data.orders_by_size).map(([key, value]) => ({
            label: key, 
            value: value
        })) : []
    })
}]

for (const item of items){
    registry.category("awesome_dashboard").add(item.id, item)
}