console.log('Eureka')

odoo.define('insca3.check_ptg', function (require){
    "use strict";

    var ajax = require('web.ajax');
    var ListController = require('web.ListController');
    var rpc = require('web.rpc')

    ListController.include({
        renderButtons: function($node) {
            this._super.apply(this, arguments);
            var self = this;
            if (this.$buttons) {
                $(this.$buttons).find('.oe_new_custom_button_insca').on('click', function() {
                    rpc.query({
                        model: 'mrp.workorder',
                        method: 'check_dir',
                        args: [],
                    }).then(function(res){
                        console.log(res)
                        self.reload();
                    })
                });
            }
        },
    });
});