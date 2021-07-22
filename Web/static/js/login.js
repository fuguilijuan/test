function login() {
    let name = document.getElementById('u').value;
    let pwd = document.getElementById('p').value;
    if (name!=="" && pwd!==""){
        let url= "http://127.0.0.1:5000/login"
        let data={
            name:name,
            pwd:pwd
        }
        $.ajax({
            type:"POST",
            contentType:"application/x-www-form-urlencoded; charset=utf-8",
            url:url,
            data:JSON.stringify(data),
            async:true,
            dataType:"json",
            success:function (result) {
                if (result.code===0){
                    alert('登录成功！')
                }
                else {
                    alert('用户名或密码错误！')
                    location.reload()
                }
            },
            error: function(XMLHttpRequest, textStatus) {
                console.log(XMLHttpRequest.status,XMLHttpRequest.readyState,textStatus)
                alert('挂了')
        }})
    }
    else {
        alert('用户名或密码不能为空！')
        location.reload()
    }
}

function errmsg() {
    document.getElementById('showerr').style.display='none'
}