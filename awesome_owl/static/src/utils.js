import { useRef, onMounted } from "@odoo/owl";

export function autoFocus(refName) {
    const input_ref = useRef(refName);

    onMounted(() => {
        input_ref.el.focus();
    });
}