$('#auth-button').click(
    function() {
        let email = $('#email').val();
        let password = $('#password').val();
        let authButton = $('#auth-button');
        const CSRF = $('[name=csrfmiddlewaretoken]').val();
        
        if(!email) {
            alert('Введите адрес электронной почты!');
        }

        if(!password) {
            alert('Введите пароль!');
        }

        let userData = {
            'email' : email,
            'password' : password,
            'csrfmiddlewaretoken': CSRF
        }

        $.ajax({
            url: '/auth/',
            type: 'POST',
            dataType: 'json',
            data: userData,

            success: function(data) {
                console.log(data);
                authButton.text('Успешно');
                authButton.prop('disabled', true);
                authButton.css({
                    'background-color': '#4CAF50',
                    'color': '#fff',
                });
                console.log('Нашелся пользователь')
                window.location.href = '/'; //Переход на главную сайта
            },
            error: function(error) {
                console.error('Error: ', error);
                alert('Нет такого пользователя');
                authButton.css({
                    'background-color': '#af4c4f',
                    'color': '#fff',
                });
                window.location.href = '/auth';
            },
        });
    }
);