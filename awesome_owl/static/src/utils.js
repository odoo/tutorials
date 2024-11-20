import { useRef, onMounted } from "@odoo/owl";

export function useFocus(refName) {
    const ref = useRef(refName);
    onMounted(
        () => {
            ref.el.focus();
        }
    )
};