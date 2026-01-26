import { useService } from "@web/core/utils/hooks";
import { useState } from "@odoo/owl";

export function useClicker() {
    let service = useService("clicker");

    return useState(service.clicker)
}
