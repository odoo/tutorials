import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";
import { registry } from "@web/core/registry";

const dashboardItems = [
    {
        id: "average_quantity",
        description: "Average T-shirt Quantity",
        Component: NumberCard,
        props: (statistics) => ({
            title: "Average amount of t-shirt by order this month",
            value: statistics.average_quantity,
            icon: "shopping-basket",
            color: "primary"
        })
    },
    {
        id: "average_time",
        description: "Average Processing Time",
        Component: NumberCard,
        props: (statistics) => ({
            title: "Average time for an order to be processed",
            value: statistics.average_time,
            icon: "clock-o",
            color: "info",
            suffix: "hrs"
        })
    },
    {
        id: "number_new_orders",
        description: "New Orders This Month",
        Component: NumberCard,
        props: (statistics) => ({
            title: "Number of new orders this month",
            value: statistics.nb_new_orders,
            icon: "shopping-cart",
            color: "success"
        })
    },
    {
        id: "cancelled_orders",
        description: "Cancelled Orders This Month",
        Component: NumberCard,
        props: (statistics) => ({
            title: "Number of cancelled orders this month",
            value: statistics.nb_cancelled_orders,
            icon: "times-circle",
            color: "danger"
        })
    },
    {
        id: "amount_new_orders",
        description: "Total Order Amount",
        Component: NumberCard,
        props: (statistics) => ({
            title: "Total amount of new orders this month",
            value: statistics.total_amount,
            icon: "money",
            color: "success"
        })
    },
    {
        id: "pie_chart",
        description: "Shirt Orders by Size",
        Component: PieChartCard,
        size: 2,
        props: (statistics) => ({
            title: "Shirt orders by size",
            values: statistics.orders_by_size,
        })
    }
];

// Register all dashboard items
dashboardItems.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
});
