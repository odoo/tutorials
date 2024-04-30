/** @odoo-module **/

import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";

const ClickerService = {
    start(env) {
        const state = reactive({ score: 0 });

        function incrementScore(inc) {
            state.score += inc;
        }

        document.addEventListener("click", () => incrementScore(1), { capture: true });

        return {
            state,
            incrementScore,
        }
    }
}

registry.category("services").add("clicker_service", ClickerService)