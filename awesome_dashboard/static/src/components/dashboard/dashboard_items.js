import { NumberCard } from "./numberCard/numberCard";
import { PieChartCard } from "./pieChartCard/pieChartCard";
import { registry } from "@web/core/registry";

const items = [
    { 
        id: "number_of_new_orders",
        component: NumberCard,
        description: "Number of new orders",
        props: (data) => ({ 
            title: "New Orders",
            value: data.nb_new_orders }),
        size: 10 
    },
    { 
        id: "total_amount",
        component: NumberCard,
        description: "Total amount of sales",
        props: (data) => ({ 
            title: "Total Sales",
            value: data.total_amount }),
        size: 10 
    },
    { 
        id: "average_order_duration",
        component: NumberCard,
        description: "Average duration till confirmation or cancellation",
        props: (data) => ({ 
            title: "Avg. Order Duration",
            value: data.average_time }),
        size: 10 
    },
    { 
        id: "average_tshirt_amount",
        component: NumberCard,
        description: "Average amount of sold t-shirts",
        props: (data) => ({ 
            title: "Avg. amount of T-shirts",
            value: data.average_quantity }),
        size: 10 
    },
    { 
        id: "number_of_cancelled_orders",
        component: NumberCard,
        description: "Total number of cancelled orders",
        props: (data) => ({ 
            title: "Number of Cancelled Orders",
            value: data.nb_cancelled_orders }),
        size: 10 
    },
    { 
        id: "size_distribution",
        component: PieChartCard,
        description: "Distribution of t-shirt sizes sold",
        props: (data) => ({ 
            title: "T-shirt Size Distribution",
            values: data.orders_by_size }),
        size: 20 
    },
]

items.forEach(item => registry.category("awesome_dashboard").add(item.id, item));
