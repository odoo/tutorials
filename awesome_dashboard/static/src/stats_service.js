
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";


const test = () => {return [['test', 2], ['test2', 3]];}

const getValues = async () => {return await rpc('/awesome_dashboard/statistics')};

export const StatsService = {
    start() {
        const getValuesMem = memoize(getValues);
        return { test, getValues, getValuesMem  };
    }
}

registry.category("services").add("awesome_dashboard.stats", StatsService);
