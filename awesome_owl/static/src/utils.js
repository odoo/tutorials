import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus() {
    const ref = useRef("inputRef");
    
    onMounted(() => {
        if (ref.el) {
            ref.el.focus();
        }
    });

    return ref;
}
