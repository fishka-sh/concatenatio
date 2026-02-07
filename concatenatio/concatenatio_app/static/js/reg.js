$('#reg-button').click(
    function() {
        let email = $('#email').val();
        let num = $('#num').val();
        let password = $('#password').val();
        let name = $('#name').val();
        let name2 = $('#name2').val();
        let tg = $('#tg').val();
        let regButton = $('#reg-button')

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
            'name' : name,
            'name2' : name2,
            'tg' : tg,
            'csrfmiddlewaretoken': CSRF
        }
        $.ajax({
            url: '/reg/',
            type: 'POST',
            dataType: 'json',
            data: dataUser,

            success:
                function(data) {
                    console.log('Success: ', data);
                    regButton.text('Отправлено');
                    regButton.prop('disabled', true);
                    regButton.css({
                        'background-color':'rgb(138, 145, 194)',
                        'color': '#fff',
                    
                    });
                    window.location.href = '/'; //Переход на главную сайта   
                },
            error:
                function(data) {
                    console.log('Success: ', data);
                    regButton.text('Нет такого пользователя');
                    regButton.prop('disabled', true);
                    regButton.css({
                        'background-color':'rgb(152, 82, 98)',
                        'color': '#fff',
                    });
                }
        });
    }
);