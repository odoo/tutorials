import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions"
import { rpc } from "@web/core/network/rpc";

const fetchData = async () => {
    return await rpc('/awesome_dashboard/statistics')
}

const memoizedFetchData = memoize(fetchData);

const myService = {
    dependencies: [],
    start(env) {
        return {
            getData: async () => {
                return await memoizedFetchData();
            },
        };

    },

};

registry.category("services").add("loadStatistics", myService);