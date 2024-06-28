/** @odoo-module **/

import { useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export function useClicker() {   
    return useState(useService("awesome_clicker.clicker"));
}
