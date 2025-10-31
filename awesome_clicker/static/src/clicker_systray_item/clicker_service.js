import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

export const clickerService = {
    start() {
        
        const count = reactive({ clicks: 0 });

        function increment(c) {
            count.clicks+= c;
        }
        
        document.addEventListener("click", () => increment(1), true);

        return {
            count,
            increment,
        };  
    },
};

registry.category("services").add("awesome_clicker.clicker", clickerService);
