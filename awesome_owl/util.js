import { onMounted, useRef } from "@odoo/owl";

export function useAutoFocus(refName) {
    const ref = useRef(refName);

    onMounted(() => {
        if (ref.el) {
            ref.el.focus()
        }
    })

    return ref;
}
