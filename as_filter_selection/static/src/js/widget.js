// Part of Alien Software - aliensoftware.dev
odoo.define('alsw_filter_selection.dynamic_selection', function(require) {
    "use strict";

    var relational_fields = require('web.relational_fields');
    var field_registry = require('web.field_registry');
    var Domain = require('web.Domain');
    var pyUtils = require('web.py_utils');

    var DynamicSelection = relational_fields.FieldSelection.extend({
        resetOnAnyFieldChange: true,

        _dynamic_selection: function(){
            if('alsw' in this.attrs){
                var alsw = pyUtils.py_eval(this.attrs.alsw);
                for(var i=0 ; i < alsw.length; i++){
                    var filter = alsw[i];
                    if('domain' in filter && 'values' in filter){
                        var check = new Domain(filter.domain).compute(this.record.data);
                        if(check){
                            var keep_values = filter.values;
                            var default_values = this.values;
                            for(var j=0; j < default_values.length; j++){
                                if(default_values[j][0] == false){
                                }
                                else if(!(keep_values.includes(default_values[j][0]))){
                                    this.$el.find("option[value='\"" + default_values[j][0] +"\"']").remove();
                                }
                            }
                        }
                    }
                }
            }
        },

        _reset: function() {
            this._super.apply(this, arguments);
            this._dynamic_selection();
            this.reset_el = this.$el;
        },

        _renderEdit: function (){
            this._super.apply(this, arguments);
            this._dynamic_selection();
        },

    });

    field_registry.add('dynamic_selection', DynamicSelection);
    return DynamicSelection;
});