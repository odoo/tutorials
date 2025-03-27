import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

const cache = reactive({values: null}, () => {
    if (callback) {
        callback(cache.values);
    }

});
let isActive = true;
let callback = null;

const nextReload = () => {
    setTimeout(async () => {
        
        if (isActive) {
            nextReload();
            cache.values = await rpc('/awesome_dashboard/statistics');
        }

    }, 600000);
}

const setActive = (cb) => {isActive = true;nextReload();callback = cb;};
const clearActive = () => {isActive = false;callback = null};

const test = () => {return [['test', 2], ['test2', 3]];}

const getValues = async () => {
    if (cache.values == null) {
        cache.values = await rpc('/awesome_dashboard/statistics');
    }

    return cache.values;
};

export const StatsService = {
    start() {
        return { test, getValues, setActive, clearActive };
    }
}

registry.category("services").add("awesome_dashboard.stats", StatsService);
