var server_url = "http://localhost:5000";

$(document).ready(function () {
    //Setting click handlers for buttons


    $('.navbar-nav').on('click', 'li > a', null, function(event) {
        event.preventDefault();

        var selection = $(event.currentTarget).attr('id');

        TableController.change_selected_table(selection)

    });


    $('#general_modal_submit_button').click(function(){
        GenericModal.submit_modal();
    });

    $('#refresh_table_button').click(function(){
        TableController.refresh_current_table_data();
    });

    $('#users').click();

});


var DataContainer = {
    /**
    * This class contains all data and handles AJAX-requests when data must be updatet
    */

    raw_user_data: "",
    raw_card_data: "",
    raw_register_data: "",
    raw_account_data: "",
    raw_transaction_data: "",

    /**
     * Updates user data and refresh table if given parameter is not null
     */

    update_raw_user_data: function (updateTableOnCallback = null) {
        //todo error cases

        AjaxRequest("/users", "GET", function (resultdata) {
            DataContainer.raw_user_data = resultdata;

            if(updateTableOnCallback != null){
                TableController.refresh_table();
            }
        });
    },

    /**
     * Updates card data and refresh table if given parameter is not null
     */
    update_raw_card_data: function (updateTableOnCallback = null) {
        //todo error cases

        AjaxRequest("/cards", "GET", function (resultdata) {
            DataContainer.raw_card_data = resultdata;

            if(updateTableOnCallback != null){
                TableController.refresh_table();
            }
        });
    },

    /**
     * Updates register data and refresh table if given parameter is not null
     */
    update_raw_register_data: function (updateTableOnCallback = null) {
        //todo error cases

        AjaxRequest("/registers", "GET", function (resultdata) {
            DataContainer.raw_register_data = resultdata;

            if(updateTableOnCallback != null){
                TableController.refresh_table();
            }
        });
    },

    /**
     * Updates account data and refresh table if given parameter is not null
     */
    update_raw_account_data: function (updateTableOnCallback = null) {
        //todo error cases

        AjaxRequest("/accounts", "GET", function (resultdata) {
            DataContainer.raw_account_data = resultdata;

            if(updateTableOnCallback != null){
                TableController.refresh_table();
            }
        });
    },

    /**
     * Updates transaction data and refresh table if given parameter is not null
     */
    update_raw_transaction_data: function (updateTableOnCallback = null) {
        //todo error cases

        AjaxRequest("/transactions", "GET", function (resultdata) {
            DataContainer.raw_transaction_data = resultdata;

            if(updateTableOnCallback != null){
                TableController.refresh_table();
            }
        });

    },

    /**
     * Updates all possible data, used when site is first time loaded
     */
    update_all_raw_data: function () {
        this.update_raw_user_data();
        this.update_raw_card_data();
        this.update_raw_account_data();
        this.update_raw_register_data();
        this.update_raw_transaction_data();

    }

};

/**
 * Generic AJAX function, sends ajax request with specified method and url and success callback
 * @param {String} url
 * @param {String} method
 * @param {Function} callback
 */
function AjaxRequest(url, method, callback) {
    $.ajax({
        url: server_url + url,
        method: method,
        success: function (data, status, xhr) {
            callback(data);
        },
        error: function (data, status, xhr) {
        }
    });
}

var TableController = {
    /**
     * This class contains all relevant functions for showing and changing table that user wants to see
     */
    selected_table: "",

    /**
     * Function that parses and shows data for table that is currently selected
     */
    refresh_table: function () {

        // Clear table and buttons under it
        $("#generic_data_table").find("tr").remove();
        $("#table_container").find(".createButton").remove();

        var data = this.get_selected_table_data();

        if (!$.isArray(data)){
            for (var item in data){
                if (data.hasOwnProperty(item) && $.isArray(data[item])){
                    data = data[item];
                }
            }
        }

        // Loop and parse data from mason objects

        var parsedData = [];
        var parsedHeaders = [];

        // Creating callbacks for buttons must be created outside loop
        function createDeletePatchCreateCallback( controlObject ){
            return function(){
                GenericModal.intialize_settings(controlObject, true);
            }
        }

        var $createButton = "";

        $.each(data, function (i, item) {
            var parsedItem = {};
            for (var key in item) {
                if (item.hasOwnProperty(key)){
                    if (key.charAt(0) != "@"){
                        if (typeof item[key] === "object"){
                            if ($.isArray(item[key])){
                                // get subitemcount (like cards and stuff)
                                if (parsedHeaders.indexOf(key) < 0) {
                                    parsedHeaders.push(key);
                                }
                                parsedItem[key] = item[key].length;
                            } else {
                                var deepItem = item[key];
                                for (var deepKey in deepItem){
                                    if (deepItem.hasOwnProperty(deepKey) && deepKey.charAt(0) != "@" && deepKey != "title") {
                                        if (parsedHeaders.indexOf(deepKey) < 0) {
                                            parsedHeaders.push(deepKey);
                                        }
                                        parsedItem[deepKey] = deepItem[deepKey];
                                    }
                                }
                            }
                        } else {
                            if (parsedHeaders.indexOf(key) < 0) {
                                parsedHeaders.push(key);
                            }
                            parsedItem[key] = item[key];
                        }
                    }
                    if (key === "@controls"){
                        var controls = item[key];
                        for (var control in controls){
                            if (controls.hasOwnProperty(control)) {
                                if (control.lastIndexOf("cr:", 0) === 0){
                                    if (controls[control].method === "DELETE" || controls[control].method === "PATCH"){
                                        if (parsedHeaders.indexOf("@" + controls[control].method) < 0) {
                                            parsedHeaders.push("@" + controls[control].method);
                                        }

                                        var buttonClass = 'btn btn-info';
                                        var buttonText = "";

                                        if (controls[control].method === "DELETE" ){
                                            buttonClass = 'btn btn-danger';
                                            buttonText = "DELETE";
                                        }

                                        if (controls[control].method === "PATCH" ){
                                            buttonClass = 'btn btn-warning';
                                            buttonText = "EDIT";
                                        }

                                        var $button = $('<button>').attr({
                                            type: 'button',
                                            class: buttonClass
                                        }).append(buttonText);

                                        var buttonTargetControl = controls[control];

                                        $button.click(createDeletePatchCreateCallback(buttonTargetControl));

                                        parsedItem["@" + controls[control].method] = $button;

                                    } else if (controls[control].method === "POST"){
                                        if ($createButton == ""){
                                            var $cbutton = $('<button>').attr({
                                                type: 'button',
                                                class: 'btn btn-primary createButton'
                                            }).append("CREATE");

                                            var createControl = controls[control];
                                            $cbutton.click(createDeletePatchCreateCallback(createControl));
                                            $createButton = $cbutton;
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            parsedData.push(parsedItem);
        });

        // Sort table columns to custom order

        parsedHeaders.sort();
        parsedHeaders.reverse();

        // Custom sorting function
        function headerSort(a,b) {
            var valueArray = ["user_id", "account_id", "balance_change", "name", "balance", "email",
                "type", "phone", "card_sha", "register_sha", "@PATCH", "@DELETE" ];

            if((valueArray.indexOf(a)) == -1 || (valueArray.indexOf(b) == -1) ){
                return 0;
            }
            return valueArray.indexOf(a) - valueArray.indexOf(b);
        }

        parsedHeaders.sort(headerSort);

        //Remove useless column that API returns for some reason
        var index = parsedHeaders.indexOf("accounts");

        if (index > -1) {
            parsedHeaders.splice(index, 1);
        }

        // Print table headers
        var $theader = $('<tr>');
        for (var title = 0; title < parsedHeaders.length; title++) {
            $theader.append($('<td>').text(parsedHeaders[title].replace("_", " ")));
        }
        $theader.appendTo("#generic_data_table > thead");


        // Print table body
        $.each(parsedData, function (i, item) {
            var $tr = $('<tr>');
            for (var j = 0; j < parsedHeaders.length; j++) {
                var key = parsedHeaders[j];
                if (key in item){
                    //$tr.append($('<td>').text(item[key]))
                    $tr.append($('<td>').append(item[key]));
                } else {
                    $tr.append($('<td>'))
                }
            }
            $tr.appendTo("#generic_data_table > tbody");
        });

        // Create button under table
        $("#button_container").prepend($createButton);
    },


    /**
     * Function for changing table that is currently seen by user
     * @param {String} new_table
     */
    change_selected_table: function (new_table) {
        this.selected_table = new_table;
        this.refresh_table();
    },

    /**
     * Function for fetching data of selected table from DataContainer object
     */
    get_selected_table_data: function (){
        var selected_table = this.selected_table;

        if (selected_table == "users"){
            return DataContainer.raw_user_data;
        }

        if (selected_table == "cards"){
            return DataContainer.raw_card_data;
        }

        if (selected_table == "accounts"){
            return DataContainer.raw_account_data;
        }

        if (selected_table == "registers"){
            return DataContainer.raw_register_data;
        }

        if (selected_table == "transactions"){
            return DataContainer.raw_transaction_data;
        }
        
        return "";
    },

    /**
     * Function for sending updating request of data to DataContainer and refreshing currently seen table
     */
    refresh_current_table_data: function () {
        var selected_table = this.selected_table;

        if (selected_table == "users"){
            DataContainer.update_raw_user_data(true);
        }

        if (selected_table == "cards"){
            DataContainer.update_raw_card_data(true);
        }

        if (selected_table == "accounts"){
            DataContainer.update_raw_account_data(true);
        }

        if (selected_table == "registers"){
            DataContainer.update_raw_register_data(true);
        }

        if (selected_table == "transactions"){
            DataContainer.update_raw_transaction_data(true);
        }
    }
};


var GenericModal = {
    /**
     * Class for generic modal
     * Builds and shows modal dynamically when it is needed
     */

    modal_id : "#generic_modal",
    target_url : "/users",
    raw_schema : "schema from url",
    schema_url : "url of raw schema",
    method : "POST",
    modal_title : "",

    /**
     * Function for initializing and showing modal
     * Builds modal dynamically based on earlier adjusted settings
     */
    initialize_modal : function(){
        var properties = this.raw_schema["properties"];
        var dialog = $(this.modal_id);

        // Clear modal and add fields that are specified in schema
        // Schemas specified descriptions, datatypes and example values are shown in dialog

        dialog.find(".modal-title").empty();
        dialog.find(".modal-title").append(this.modal_title);

        dialog.find(".form-group").empty();

        $.each(properties, function (i, item) {
            var $textinput = $('<input>');

            var maxLen = 1000;

            if (item.maxLength != null) {
                maxLen = item.maxLength;
            }

            $textinput.attr({
                type: 'text',
                class: 'form-control',
                id: "generic_modal_" + i,
                placeholder: "Example: " + item.example,
                maxLength: maxLen
            });

            //Does not work completely, but giver error tooltip is length is too short
            if (item.minLength != null) {
                var pat = ".{" + item.minLength +",}";
                $textinput.attr({pattern: pat});
            }

            var $labelfortextinput = $('<label>');

            $labelfortextinput.attr({
                for: "generic_modal_" + i
            });

            $labelfortextinput.append(item.description);

            dialog.find(".form-group").append($labelfortextinput);
            dialog.find(".form-group").append($textinput);
        });

        dialog.modal('show');
    },

    /**
     * Function for submitting modal
     * Dynamically runs ajax request that is built by pre-set schema from mason object controls
     * In case of error or bad request shows error message
     */
    submit_modal : function(){
        var data = {};
        var properties = this.raw_schema["properties"];
        var dialog = $(this.modal_id);

        // Loop through properties of payload schema and dialog filled fields to create payload for ajax request

        $.each(properties, function (i, item) {
            var field_id = "#generic_modal_" + i;
            var v = dialog.find(field_id).val();

            if(item.type == "integer"){
                data[i] = parseInt(v);
            }else if(item.type == "double"){
                data[i] = parseFloat(v);
            }else{
                data[i] = v;
            }
        });

        $.ajax({
            url: server_url + GenericModal.target_url,
            method: GenericModal.method,
            data: JSON.stringify(data),
            contentType: "application/json",
            success: function (data, status, xhr) {
                TableController.refresh_current_table_data();
            },
            error: function (data, status, xhr) {
                alert(data.status + " " + data.statusText + " Details: " + data.responseJSON.detail);
            }
        });
    },

    /**
     * Function for initializing object settings.
     * Gets control object of mason-object and initializes modal and makes ajax request to get control payload schema
     * If second parameter is not null, modal is shown after initialization is ready
     *
     * @param {String} control_object
     * @param {Object} showModalOnReady
     */
    intialize_settings : function(control_object, showModalOnReady = null) {
        this.set_target_url(control_object.href);
        this.method = control_object.method;
        this.modal_title = control_object.title;

        if(control_object.schema_url){
            this.set_schema(control_object.schema_url, showModalOnReady);
        } else {
            this.raw_schema = "";
            if(showModalOnReady != null){
                GenericModal.initialize_modal();
            }
        }
    },

    /**
     * Function for getting payload schema and storing it in this object
     * If second parameter is not null, modal is shown after initialization is ready
     *
     * @param {String} schema_url
     * @param {Object} showModalOnReady
     */
    set_schema : function(schema_url, showModalOnReady = null) {
        AjaxRequest(schema_url, "GET", function (resultdata) {
            GenericModal.raw_schema = resultdata;

            if(showModalOnReady != null){
                GenericModal.initialize_modal();
            }
        });

    },

    /**
     * Function for setting modal submission target url
     * Because API does return odd URLs, removing part of them is required to make client work
     *
     * @param {String} url
     */
    set_target_url : function(url){
        this.target_url = url.replace('patch/','').replace('delete/','');
    }

};


DataContainer.update_all_raw_data();