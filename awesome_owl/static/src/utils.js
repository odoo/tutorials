import { onMounted, useRef } from "@odoo/owl";

export function useAutoFocus(name) {
    let inputFocus = useRef(name);
    onMounted(() => {
        inputFocus.el.focus()
    })
}
