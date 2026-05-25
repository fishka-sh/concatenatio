$('#confirm-button').click(
    function() {

        // Подбираем данные с HTML
        let emailCode = $('#email-code').val();
        let confirmButton = $('#confirm-button');

        confirmButton.prop('disabled', true);
        $('.confirm').append(`
            <div id="confirm-spinner" class="spinner-border mt-2" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        `)

        const CSRF = $('[name=csrfmiddlewaretoken]').val();
        
        let userData = {
            'email-code' : emailCode,
            'csrfmiddlewaretoken': CSRF
        }

        $.ajax({
            url: '/confirm/',
            type: 'POST',
            dataType: 'json',
            data: userData,

            success: function(data) {
                window.location.href = '/';
            },

            error: function(xhr) {
                if(xhr.responseJSON) {
                    $('#confirm-spinner').remove();
                    $('#error-message').remove();
                    $('.confirm').append(`
                        <div id="error-message" class="alert alert-danger" role="alert">
                            ${xhr.responseJSON.message}
                        </div>
                    `);
                    confirmButton.prop('disabled', false);
                }
            }   
        });
    }
);
