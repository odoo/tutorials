import { registry } from "@web/core/registry"
import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";

const dashboard_registry = registry.category("awesome_dashboard")
dashboard_registry.add("average_new_order",{
    id: "average_new_order",
    description: "Average amount of new orders",
    Component: NumberCard,
    props: (data) => ({
        title: "Average amount of new orders this month",
        value: data.total_amount
    }),
});
dashboard_registry.add("number_new_order",{
    id: "number_new_order",
    description: "Total amount of new orders",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Total amount of new orders this month",
        value: data.nb_new_orders
    }),
});
dashboard_registry.add("average_quantity",{
    id: "average_quantity",
    description: "Average amount of t-shirt",
    Component: NumberCard,
    size: 5,
    props: (data) => ({
        title: "Average amount of t-shirt by order this month",
        value: data.average_quantity
    }),
});
dashboard_registry.add("number_cancelled_order",{
    id: "number_cancelled_order",
    description: "Number of cancelled orders",
    Component: NumberCard,
    size: 2,
    props: (data) => ({
        title: "Number of cancelled orders this month",
        value: data.nb_cancelled_orders
    }),
});
dashboard_registry.add("average_state_change",{
    id: "average_state_change",
    description: "Average time for state change",
    Component: NumberCard,
    props: (data) => ({
        title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
        value: data.average_time
    }),
});
dashboard_registry.add("pie_chart",{
    id: "pie_chart",
    description: "Shirt orders by size",
    Component: PieChartCard,
    size: 3,
    props: (data) => ({
        title: "Shirt orders by size",
        value: data.orders_by_size
    }),
});
