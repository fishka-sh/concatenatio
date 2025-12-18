$('#enter-button').click(
    function() {
        let email = $('#email').val();
        let num = $('#num').val();
        let password = $('#password').val();
        const CSRF = $('[name=csrfmiddlewaretoken]').val();

        if(!email) {
            alert('Введите адрес электронной почты');

        }
        if(!num) {
            alert('Введите пароль');
        }
        let dataUser = {
            'email' : email,
            'num' : num,
            'password' : password,
            'csrfmiddlewaretoken': CSRF
        }
        $.ajax({
            url: '/enter/',
            type: 'POST',
            dataType: 'json',
            data: dataUser,
        });
    }
);