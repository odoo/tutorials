import { onMounted } from "@odoo/owl";

export function useAutofocus(myRef){
    onMounted(() => {
        if(myRef){
            myRef.el.focus();
        }
    });    
}
