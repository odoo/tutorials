/** @odoo-module **/

import { onMounted } from '@odoo/owl';

export function useAutofocus(ref){
    onMounted(()=>{
        if(ref){
            ref.el.focus();
        }
    })
}
