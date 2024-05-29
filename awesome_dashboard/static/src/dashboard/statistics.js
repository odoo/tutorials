/** @odoo-module **/

import { registry } from "@web/core/registry";
import { reactive, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export const useStatistics = () => {
    return useState(useService("awesome_dashboard.statistics"));
};

const statisticsService = {
    dependencies: ["rpc"],
    start: async (env, { rpc }) => {
        const statistics = await rpc("/awesome_dashboard/statistics");
        const reactiveStatistics = reactive(statistics);
        const updateData = async () => {
            const updatedStatistics = await rpc("/awesome_dashboard/statistics");
            Object.assign(reactiveStatistics, updatedStatistics);
        };

        setInterval(updateData, 10 * 60 * 1000);

        return reactiveStatistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);