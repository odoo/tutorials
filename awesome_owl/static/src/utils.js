import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(refName) {
    const ref = useRef(refName);
    onMounted(() => {
        console.log(ref.el);
        ref.el.focus();
    });
}