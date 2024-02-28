/**@odoo-module */
import { useService } from "@web/core/utils/hooks";
import { useState } from "@odoo/owl";

export const useClicker = () => {
    return useState(useService("clickerService"));
}