odoo.define('alsw.field_utils', function (require) {
    "use strict";

    var fu = require('web.field_utils');
    var core = require('web.core');
    var dom = require('web.dom');
    var session = require('web.session');
    var time = require('web.time');
    var utils = require('web.utils');

    var _t = core._t;

    function formatTime(value, field, options) {
        if (value === false) {
            return "";
        }
        return value;
    }

    function parseTime(value, field, options) {
        if (!value) {
            return false;
        }
        //
        var timePattern = time.getLangTimeFormat();
        return moment('1970-01-01 ' + value).format(timePattern);
    }

    fu.format.__defineGetter__('time', function() {
        return formatTime;
    });

    fu.parse.__defineGetter__('time', function() {
        return parseTime;
    });

});