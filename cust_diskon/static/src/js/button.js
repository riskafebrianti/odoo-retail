odoo.define("cust_diskon.button", function(require) {
'use strict';
    
    const PosComponent = require("point_of_sale.PosComponent");
    const ProductScreen = require("point_of_sale.ProductScreen");
    const Registries = require("point_of_sale.Registries");
    const { useListener } = require("@web/core/utils/hooks");

    class button extends PosComponent{

        setup(){
            super.setup();
            useListener("click", this.buttontes);
        }
       
        
        async buttontes(){
            // console.log("tes tess");
            this.showPopup("ConfirmPopup",{
                title : "ini popup",
                body : "jejeng",

            });
        }
    }

    button.template = "button";
    ProductScreen.addControlButton({
        component: button,
        position : ["before","OrderlineCustomerNoteButton"],
    });
    
    Registries.Component.add(button);

    return button;
});