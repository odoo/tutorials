/** @odoo-module **/

import { useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export function useClicker() {
    const clickerService = useService("clicker");
    const clicker = useState(clickerService)

    return clicker;
}