import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsService = {
    start() {
        const stats = reactive({});

        let isStopped = false;

        async function load() {
            try {
                const result = await rpc("/awesome_dashboard/statistics", {});
                Object.assign(stats, result);
            } catch (error) {
                console.error("Failed to load dashboard stats:", error);
            }
        }

        async function loop() {
            if (isStopped) return;
            await load();
            setTimeout(loop, 10000);
        }
        loop();
        return {
            stats,
            stop() {
                isStopped = true;
            },
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService)
