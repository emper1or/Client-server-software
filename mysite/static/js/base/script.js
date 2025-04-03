document.addEventListener('DOMContentLoaded', function () {
    const togglePassword = document.getElementById('togglePassword');
    const password = document.getElementById('password');

    if (togglePassword && password) {
        togglePassword.addEventListener('click', function () {
            const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
            password.setAttribute('type', type);

            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
        });
    }
});

function refresh_captcha()
{
    $.ajax({
    type:"GET"
    url: "/captcha_images.php?width=120&height=40&code=$code"?>'
    success: function(msg)
   {
    document.getElementById ("captcha_img").src = msg;
   },
error:functon(){alert("some error occured");}
     });

}