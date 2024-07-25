/** @odoo-module **/

import { reactive } from "@odoo/owl";
import { memoize } from "@web/core/utils/functions";
import { registry } from "@web/core/registry";

import { buildDynamicComponentList } from "../dashboard/dashboard_utils";


const formatData = (data) => {
    return Object.entries(data).map(([key, value]) => {
        const name = key.split('_').map(e => e[0].toUpperCase() + e.slice(1)).join(' ')
        if (typeof value !== 'object') return { name, key, value, view: 'view' };
        return { key, name, value, view: 'chart' };
    });
}

const statisticsService = {
    dependencies: ["rpc"],
    start(env, { rpc }) {
        const memoizedRpc = memoize(rpc);

        const context = {
            path: null,
            state: reactive({
                values: [], currentTime: '', hiddenIds: []
            }),
            loadStatistics: async function (path) {
                if (path) this.path = path;
                const hours = new Date().getHours().toString().padStart(2, '0');
                const minutes = new Date().getMinutes().toString().padStart(2, '0');
                const seconds = new Date().getSeconds().toString().padStart(2, '0')
                this.state.values = buildDynamicComponentList(formatData(await rpc(this.path)));
                this.state.currentTime = `${hours}:${minutes}:${seconds}`
                return this.state;
            },
            getState: function () {
                return this.state;
            },
            setHiddenItems: function (hiddenIds) {
                localStorage.setItem('items', JSON.stringify(hiddenIds));
                this.loadStatistics()
            },
        }

        setInterval(async () => {
            context.loadStatistics()
        }, 1000);

        return context;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);