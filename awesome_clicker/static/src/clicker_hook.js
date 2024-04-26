/** @odoo-module **/

import { useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export function useClicker() {
    const service = useService("awesome_clicker.service");
    const state = useState(service.state);

    return { 
        state, 
        increment: service.increment,
    };;
  }
