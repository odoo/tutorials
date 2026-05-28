import { onMounted, useRef } from "@odoo/owl"


export function Autofocus(refName) {
    const ref = useRef(refName);

    onMounted(() => {
        ref.el.focus()
    })
}
