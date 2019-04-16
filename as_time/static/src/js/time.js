odoo.define('alsw.time', function(require) {
    "use strict";


    var basic_fields = require('web.basic_fields');
    var field_registry = require('web.field_registry');
    var datepicker = require('web.datepicker');

    var FieldTime = basic_fields.InputField.extend({
        className: 'o_field_time',
        tagName: 'span',
        supportedFieldTypes: ['time'],

        _renderEdit: function () {
            this._super.apply(this, arguments);
            if(this.recordData[this.name] === false){
                this.$el.prop({value:"00:00:00"});
            }
            this.$el.prop({type:"time"});
        },

        _setValue: function (value, options) {
            if (this.field.trim) {
                value = value.trim();
            }
            return this._super(value, options);
        },
    });
    field_registry.add('time', FieldTime);

});