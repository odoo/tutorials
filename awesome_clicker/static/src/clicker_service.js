import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const clickerService = {
    start(env) {
        const state = reactive({
            clicks: 0,
            level: 0,
            clickBots: 0,
        });

        setInterval(() => {
            state.clicks += state.clickBots * 10;
        }, 10000);

        function increment(inc) {
            state.clicks += inc;
            if (state.level < 1 && state.clicks >= 1000) {
                state.level++;
            }
        }

        function buyClickBot() {
            const clickBotPrice = 1000;
            if (state.clicks < clickBotPrice) {
                return false;
            }
            state.clicks -= clickBotPrice;
            state.clickBots += 1;
        }

        document.addEventListener("click", () => increment(1), true);

        return {
            state,
            increment,
            buyClickBot,
        };
    },
};

registry.category("services").add("awesome_clicker.clicker", clickerService);
