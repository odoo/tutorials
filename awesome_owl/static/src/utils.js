import { onMounted, useRef } from "@odoo/owl"

export function useAutofocus(ref) {
    let componentRef = useRef(ref);
    onMounted(() => {
        componentRef.el.focus();
    })
}
