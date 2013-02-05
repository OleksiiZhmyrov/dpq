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
                        minlength: 3

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
                        required: "Field login is required",
                        minlength: "Login must contain not less than 3 characters"
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
                    required: true
                },
                description: {
                    required: true
                },
                devA: {
                    required: true
                }
            },
            highlight: function (label) {
                $(label).closest('.control-group').addClass('error').removeClass('success');
            },
            success: function (label) {
                label.closest('.control-group').addClass('success').removeClass('error');
            }
        });
    return $("#add-to-queue-form").valid();
}

function isValidModifyForm() {
    $("#modify-queue-form").validate(
        {
            rules: {
                ps: {
                    required: true
                },
                description: {
                    required: true
                },
                devA: {
                    required: true
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
            }
        });
    return $("#modify-queue-form").valid();
}
