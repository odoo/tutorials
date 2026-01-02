import { useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export function useClicker(){
    const state = useState(useService("awesome_clicker.clicker_service"));
    return state;
}
