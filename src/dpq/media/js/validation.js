$(document).ready(function () {

    $.validator.addMethod(
        'regexp',
        function (value, element, regexp) {
            var re = new RegExp(regexp);
            return this.optional(element) || re.test(value);
        },
        "Please check your input."
    );

    $('#register-form input[type="submit"]').click(function (e) {
        $('#register-form').validate(
            {
                onkeyup: false,
                onfocusout: false,
                rules: {
                    username: {
                        required: true,
                        minlength: 3,
                        regexp: '^[A-Za-z0-9_]+$'
                    },
                    password1: {
                        required: true,
                        regexp: '(?!^[0-9]*$)(?!^[a-zA-Z!@#$%^&*()_+=<>?]*$)^([a-zA-Z!@#$%^&*()_+=<>?0-9]{6,15})$'
                    },
                    password2: {
                        required: true,
                        equalTo: "input[name='password1']"
                    }
                },
                highlight: function (label) {
                    $(label).closest('.control-group').addClass('error').removeClass('success');
                },
                success: function (label) {
                    label.closest('.control-group').addClass('success').removeClass('error');
                },
                messages: {
                    username: {
                        required: "Field username is required",
                        minlength: "Username must contain not less than 3 characters",
                        regexp: "Username can only contain alphanumeric characters and the underscores"
                    },
                    password1: {
                        required: "Field passsword is required",
                        regexp: "Password must contain a number and an alphabet and should be more than 6 characters long"
                    },
                    password2: {
                        required: "Password confirmation is required",
                        equalTo: "Confirmation password does not match the password"
                    }
                }
            });
    });

});

function isValidCreateForm() {
    $("#add-to-queue-form").validate(
        {
            rules: {
                ps: {
                    required: true,
                    maxlength: 10,
                    regexp: '^[A-Za-z0-9_]+$'
                },
                description: {
                    required: true,
                    maxlength: 128,
                    minlength: 2
                },
                devA: {
                    required: true,
                    maxlength: 64,
                    minlength: 2,
                    regexp: '^[A-Za-z \']+$'
                },
                devB: {
                    maxlength: 64,
                    regexp: '^[A-Za-z \']+$'
                },
                tester: {
                    maxlength: 64,
                    regexp: '^[A-Za-z \']+$'
                }
            },
            highlight: function (label) {
                $(label).closest('.control-group').addClass('error').removeClass('success');
            },
            success: function (label) {
                label.closest('.control-group').addClass('success').removeClass('error');
            },
            messages: {
                ps: {
                    required: "PS code is mandatory",
                    maxlength: "Max length is 10 characters",
                    regexp: "Allowed characters are latin letters, digits and undescore"
                },
                description: {
                    required: "Description field is mandatory",
                    maxlength: "Max length is 128 characters",
                    minlength: "Description is too short!"
                },
                devA: {
                    required: "There must be at least one developer",
                    maxlength: "Max length is 64 characters",
                    minlength: "Even Chinese have names more than 2 letters long",
                    regexp: "Allowed characters are latin letters and space"
                },
                devB: {
                    maxlength: "Max length is 64 characters",
                    regexp: "Allowed characters are latin letters and space"
                },
                tester: {
                    maxlength: "Max length is 64 characters",
                    regexp: "Allowed characters are latin letters and space"
                }
            }
        });
    return $("#add-to-queue-form").valid();
}

function isValidModifyForm() {
    $("#modify-queue-form").validate(
        {
            rules: {
                ps: {
                    required: true,
                    maxlength: 10,
                    regexp: '^[A-Za-z0-9_]+$'
                },
                description: {
                    required: true,
                    maxlength: 128,
                    minlength: 2
                },
                devA: {
                    required: true,
                    maxlength: 64,
                    minlength: 2,
                    regexp: '^[A-Za-z \']+$'
                },
                devB: {
                    maxlength: 64,
                    regexp: '^[A-Za-z \']+$'
                },
                tester: {
                    maxlength: 64,
                    regexp: '^[A-Za-z \']+$'
                },
                place: {
                    required: true,
                    number: true
                }
            },
            highlight: function (label) {
                $(label).closest('.control-group').addClass('error').removeClass('success');
            },
            success: function (label) {
                label.closest('.control-group').addClass('success').removeClass('error');
            },
            messages: {
                ps: {
                    required: "PS code is mandatory",
                    maxlength: "Max length is 10 characters",
                    regexp: "Allowed characters are latin letters, digits and undescore"
                },
                description: {
                    required: "Description field is mandatory",
                    maxlength: "Max length is 128 characters",
                    minlength: "Description is too short!"
                },
                devA: {
                    required: "There must be at least one developer",
                    maxlength: "Max length is 64 characters",
                    minlength: "Even Chinese have names more than 2 letters long",
                    regexp: "Allowed characters are latin letters and space"
                },
                devB: {
                    maxlength: "Max length is 64 characters",
                    regexp: "Allowed characters are latin letters and space"
                },
                tester: {
                    maxlength: "Max length is 64 characters",
                    regexp: "Allowed characters are latin letters and space"
                },
                place: {
                    required: "Please enter desired place number",
                    number: "Must be a number"
                }
            }
        });
    return $("#modify-queue-form").valid();
}
