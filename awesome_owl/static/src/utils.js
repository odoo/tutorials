/** @odoo-module **/

import { useRef, onMounted } from "@odoo/owl";

export function useAutoFocus(ref_name) {
    const refProxy = useRef(ref_name)
    onMounted(() => {
        if (refProxy.el) {
            refProxy.el.focus()
        }
    })
}
