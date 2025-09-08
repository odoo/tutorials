import { onMounted, useRef } from "@odoo/owl";

export function useAutoFocus(elementName) {
    const ref = useRef(elementName)
    onMounted(() => {
        ref.el.focus()
    })

}
