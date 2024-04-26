/** @odoo-module **/

import { useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export function useClicker() {
    const clickerService = useService("clicker");
    const state = useState(clickerService.state);

    return {
        state: state,
        increment: clickerService.increment,
        buyClickBot: clickerService.buyClickBot
    }
}