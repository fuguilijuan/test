//
// function addClick(){
//     //判断如果配置项都填了，就显示加载中，然后调用api测试接口
//     let host = document.getElementById('host').value;
//     let port = document.getElementById('port').value;
//     let ip = document.getElementById('ip').value;
//     let name = document.getElementById('name').value;
//     let pwd = document.getElementById('pwd').value;
//     //复选框
//     let checkBox=document.getElementsByName('checkBox')[0];
//     let case_data = document.getElementById('data').innerText;
//
//     if (host===""||port===""||ip===""||name===""||pwd===""){
//         return false
//     }
//     else {
//         if (checkBox.checked===true){
//
//         }
//         else {
//
//         }
//
//         console.log("checkBox:"+checkBox.checked)
//         document.getElementById('shadow').style.display='block'
//         document.getElementById('load_gif').style.display='block'
//         setTimeout(is_sleep,300000)
//         return true
//     }
// }

function is_sleep() {
    //等待时间后隐藏gif的loading效果
    document.getElementById('shadow').style.display='none'
    document.getElementById('load_gif').style.display='none'
}

// function is_show() {
//     //数据库连接失败信息，获取焦点后隐藏
//     document.getElementById('dberr').style.display='none'
//     document.getElementById('urlerr').style.display='none'
// }

