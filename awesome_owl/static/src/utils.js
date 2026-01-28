import { useRef, onMounted } from "@odoo/owl";

export function useAutoFocus(name) {
    const ref = useRef(name);
    onMounted(() => {
        if (ref.el) {
            ref.el.focus();
        }
    });
    return ref;
}
