/** @odoo-module **/

import { registry } from "@web/core/registry";
import { memoize } from '@web/core/utils/functions';

const statistics_service = {
    dependencies: ["rpc"],
    start(env, { rpc }) {
        return {
            load: memoize(() => rpc("/awesome_dashboard/statistics")),
        }
    },
};

registry.category("services").add("awesome_dashboard.statistics", statistics_service);
