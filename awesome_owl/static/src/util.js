import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(refName) {
    let ref = useRef(refName);
    onMounted(() => {
        ref.el?.focus()
    })
}
