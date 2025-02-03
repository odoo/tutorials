import { onMounted } from "@odoo/owl";

export function useAutoFocus(ref) {
    console.log('use Auto Focus');
    onMounted(()=>{
        ref.el.focus()
    });
}