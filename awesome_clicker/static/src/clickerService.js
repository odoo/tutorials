import { registry } from "@web/core/registry";
import { ClickerModel } from "./clickerModel";
import { useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

const clickerService = {
    start(env) {
        const clickerModel = new ClickerModel({
            clicks: 990,
            level: 1,
            clickBots: 0,
        })

        document.addEventListener("click", () => clickerModel.increment(1), true);

        setInterval(() => clickerModel.computeAutoClicks(), 10000);

        return {
            clickerModel
        };
    },
};

registry.category("services").add("clickerService", clickerService);

export function useClicker() {
    const service = useState(useService("clickerService"));
    return service.clickerModel;
}