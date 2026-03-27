import { registry } from "@web/core/registry";

let value = 0;

const countService = {
    start() {
        return {
            getValue() {
                return value;
            },
            increment() {
                value++;
            }
        };
    }
};

registry.category("services").add("awesome_dashboard.count", countService);
