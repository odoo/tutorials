import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";

export const clickerService = {
    start() {
        const state = reactive({
            clicks: 0,
            level: 0,
            clickBots: 0,
        });

        function increment(val) {
            state.clicks += val;
            if (state.level < 1 && state.clicks >= 1000) {
                state.level++;
            }
        }

        function buyClickBot() {
            const botPrice = 1000;
            if (state.clicks < botPrice) {
                return;
            }

            state.clicks -= botPrice;
            state.clickBots++;
        }

        function botsDoClicks() {
            state.clicks += state.clickBots * 10;
        }

        document.addEventListener("click", () => increment(1), true);
        setInterval(botsDoClicks, 10000);
        return {
            state,
            increment,
            buyClickBot,
        };
    },
};

registry.category("services").add("awesome_clicker.game_service", clickerService);
