import {reactive} from "@odoo/owl";
import {rpc} from "@web/core/network/rpc";
import {registry} from "@web/core/registry"

async function loadStatistics() {
    const result = await rpc("/awesome_dashboard/statistics");
    return result;
}

export const statisticsService = {

    async start(env) {
        const state = reactive({resp: {}})

        async function reload() {
            state.resp = await loadStatistics();
            console.log("updating cache", JSON.stringify((state.resp)));
            return true;
        }

        state.resp = await loadStatistics();
        this.ref = setInterval(reload, 3 * 1000)
        return state;

    }

}

registry.category("services").add("awesome_owl.statistics", statisticsService);