import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { browser } from "@web/core/browser/browser";

export const statisticsService = {
    dependencies: [],
    start(env) {
        const storageKey = "awesome_dashboard.disabled_items";
        const saved = browser.localStorage.getItem(storageKey);
        const statistics = reactive({
            data: {},
            disabledItems: saved ? JSON.parse(saved) : [],
        });

        async function loadData() {
            try {
                const freshData = await rpc("/awesome_dashboard/statistics");
                Object.assign(statistics.data, freshData);
            } catch (e) {
                console.error("RPC Failed", e);
            }
        }

        function setDisabledItems(items) {
            statistics.disabledItems = items;
            browser.localStorage.setItem(storageKey, JSON.stringify(items));
        }

        loadData();
        setInterval(loadData, 10000);
        return {
            statistics,
            setDisabledItems,
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
