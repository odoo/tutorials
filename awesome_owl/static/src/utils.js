import { onMounted, useRef } from "@odoo/owl"

export function useAutoFocus(focusItem) {
    const ref = useRef(focusItem);
    onMounted(() => {
        ref.el.focus()
    })
}