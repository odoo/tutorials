import { useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export function useClicker() {
    const service = useService("awesome_clicker.game_service");
    const state = useState(service.state);

    return {
        ...service,
        state,
    };
}
