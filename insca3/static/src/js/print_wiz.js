

odoo.define('insca3.print_wiz', function (require){
    "use strict";
    // console.log('Eureka')
    var ajax = require('web.ajax');
    var FormController = require('web.FormController');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var _t = core._t;

    FormController.include({
        renderButtons: function($node) {
            this._super.apply(this, arguments);
            var self = this;
            if (this.$buttons) {
                $(this.$buttons).find('.oe_new_custom_button_insca_open_wiz').on('click', function(event) {
                event.stopPropagation();
                var action = {
                    type: 'ir.actions.act_window',
                    res_model: 'print.bom.wiz',
                    view_mode: 'form',
                    view_type: 'form',
                    // action_from: 'mail.ThreadComposeMessage',
                    views: [[2787, 'form']],
                    // "print_bom_wiz_form_view",
                    target: 'new',
                    context: {'default_bom_id': self.id},
                };
                console.log('action done')
                self.do_action(action);

               });
            }
        },
    });
});