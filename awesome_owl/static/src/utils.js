import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(name) {
    let ref = useRef(name);
    onMounted(() => {
        ref.el.focus();
    });
}
