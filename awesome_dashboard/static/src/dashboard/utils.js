import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions"
import { rpc } from "@web/core/network/rpc";
import { Numbercard } from "./number_card/number_card";
import { Piecard } from "./pie_card/pie_card";


const fetchData = async () => {
    return await rpc('/awesome_dashboard/statistics')
}

const cardItems = [
    {
        total_amount: "Total amount of new orders this month",
        component: Numbercard,
    },
    {
        nb_new_orders: "Number of new orders this month",
        size: 2,
        component: Numbercard,
    },
    {
        average_quantity: "Average amount of t-shirt by order this month",
        component: Numbercard,
    },
    {
        nb_cancelled_orders: "Number of cancelled orders this month",
        component: Numbercard,
    },
    {
        average_time:
            "Average time for an order to go from ‘new’ to ‘sent’ or ‘cancelled’",
        component: Numbercard,
    },
    {
        orders_by_size: "Shirts order by Size",
        component: Piecard,
    },
];

const memoizedFetchData = memoize(fetchData);

const myService = {
    dependencies: [],
    start() {
        return {
            getData: async () => {
                return await memoizedFetchData();
            },
            itemData: cardItems,
        };

    },

};

registry.category("services").add("loadStatistics", myService);