import { useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export const useClicker = () => {
    return useState(useService("clicker"));
};
