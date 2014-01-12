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
                        regexp: '(?!^[0-9]*$)(?!^[a-zA-Z!@#$%^&*()_+=<>?]*$)^([a-zA-Z!@#$%^&*()_+=<>?0-9]{6,25})$'
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
                        minlength: "Username must contain at least 3 characters",
                        regexp: "Username can only contain alphanumeric characters and the underscores"
                    },
                    password1: {
                        required: "Field password is required",
                        regexp: "Password must contain alphanumeric characters and should be at least 6 characters long. Max length is 25 symbols"
                    },
                    password2: {
                        required: "Password confirmation is required",
                        equalTo: "Password confirmation does not match the password"
                    }
                }
            });
    });

});

function isValidCreateForm() {
    $("#add-to-queue-form").validate(
        {
            rules: {
                key: {
                    required: true,
                    maxlength: 13,
                    regexp: '^[A-Z]{2,10}\-[0-9]{1,4}$'
                },
                summary: {
                    required: false,
                    maxlength: 256
                },
                developer: {
                    required: true,
                    maxlength: 64,
                    minlength: 2,
                    regexp: '^[A-Za-z \']+$'
                },
                tester: {
                    required: true,
                    maxlength: 64,
                    minlength: 2,
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
                key: {
                    required: "Story Key is mandatory",
                    maxlength: "Max length is 16 characters",
                    regexp: "Please enter value according to regexp: ^[A-Z]{2,12}\\-[0-9]{1,4}$"
                },
                summary: {
                    maxlength: "Max length is 256 characters"
                },
                developer: {
                    required: "Please enter name",
                    maxlength: "Max length is 64 characters",
                    minlength: "Even Chinese have names more than 2 letters long",
                    regexp: "Allowed characters are latin letters and space"
                },
                tester: {
                    required: "Please enter name",
                    maxlength: "Max length is 64 characters",
                    minlength: "Even Chinese have names more than 2 letters long",
                    regexp: "Allowed characters are latin letters and space"
                }
            },
            errorPlacement: function(error, element) {
                if (element.attr("name") == "key") {
                      error.insertAfter("#validation-msg");
                } else {
                      error.insertAfter(element);
                }
            }
        });
    return $("#add-to-queue-form").valid();
}

function isValidModifyForm() {
    $("#modify-queue-form").validate(
        {
            rules: {
                    key: {
                    required: true,
                    maxlength: 13,
                    regexp: '^[A-Z]{2,10}\-[0-9]{1,4}$'
                },
                summary: {
                    required: false,
                    maxlength: 256
                },
                developer: {
                    required: true,
                    maxlength: 64,
                    minlength: 2,
                    regexp: '^[A-Za-z \']+$'
                },
                tester: {
                    required: true,
                    maxlength: 64,
                    minlength: 2,
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
                key: {
                    required: "Story Key is mandatory",
                    maxlength: "Max length is 16 characters",
                    regexp: "Please enter value according to regexp: ^[A-Z]{2,12}\\-[0-9]{1,4}$"
                },
                summary: {
                    maxlength: "Max length is 256 characters"
                },
                developer: {
                    required: "Please enter name",
                    maxlength: "Max length is 64 characters",
                    minlength: "Even Chinese have names more than 2 letters long",
                    regexp: "Allowed characters are latin letters and space"
                },
                tester: {
                    required: "Please enter name",
                    maxlength: "Max length is 64 characters",
                    minlength: "Even Chinese have names more than 2 letters long",
                    regexp: "Allowed characters are latin letters and space"
                }
            }
        });
    return $("#modify-queue-form").valid();
}


function isValidStoryKey() {
    $("#add-to-queue-form").validate(
        {
            rules: {
                key: {
                    required: true,
                    maxlength: 13,
                    regexp: '^[A-Z]{2,10}\-[0-9]{1,4}$'
                }
            },
            highlight: function (label) {
                $(label).closest('.control-group').addClass('error').removeClass('success');
            },
            success: function (label) {
                $(label).closest('.control-group').addClass('success').removeClass('error');
            },
            messages: {
                key: {
                    required: "Story Key is mandatory",
                    maxlength: "Max length is 16 characters",
                    regexp: "Please enter value according to regexp: ^[A-Z]{2,12}\\-[0-9]{1,4}$"
                }
            },
            errorPlacement: function(error, element) {
                if (element.attr("name") == "key") {
                      error.insertAfter("#validation-msg");
                } else {
                      error.insertAfter(element);
                }
            }
        });
    return $("#add-to-queue-form").valid();
}

function retroIsValidAddForm() {
    $("#retro-add-sticker-form").validate(
        {
            rules: {
                summary: {
                    required: true,
                    maxlength: 512,
                    regexp: '^[A-Za-z0-9 \-.,;+?!]*$'
                }
            },
            highlight: function (label) {
                $(label).closest('.control-group').addClass('error').removeClass('success');
            },
            success: function (label) {
                label.closest('.control-group').addClass('success').removeClass('error');
            },
            messages: {
                summary: {
                    required: "Summary is mandatory",
                    maxlength: "Max length is 512 characters",
                    regexp: "Only digits latin letters are allowed"
                }
            },
            errorPlacement: function(error, element) {
                error.insertAfter(element);
            }
        });
    return $("#retro-add-sticker-form").valid();
}