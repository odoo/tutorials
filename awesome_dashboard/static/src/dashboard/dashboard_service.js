/** @odoo-module **/
import { registry } from "@web/core/registry";

const dashboardService = {
    start() {
        let counter = 0;

        return {
            get() {
                return counter;
            },
            inc() {
                counter += 1;
                return counter;
            },
        };
    },
};

registry.category("services").add("awesome_dashboard_service", dashboardService);
