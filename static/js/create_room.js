document.getElementById('create_room_form').addEventListener('submit', function(event) {
    event.preventDefault(); // 阻止表单提交

    var roomNumber = document.getElementById('exampleInputRoomNumber').value; // 获取房间号输入
    var password = document.getElementById('exampleInputPassword1').value; // 获取密码输入
    var roomErrorMessage = document.getElementById('roomHelp'); // 获取房间号错误消息元素
    var passwordErrorMessage = document.getElementById('passwordHelp'); // 获取密码错误消息元素

    // 验证房间号是否为四位数字
    if (!/^\d{4}$/.test(roomNumber)) {
        roomErrorMessage.textContent = "Please enter a valid four-digit room number."; // 更新房间号错误消息
        roomErrorMessage.classList.add('text-danger'); // 添加错误样式
    } else {
        roomErrorMessage.textContent = "Please enter a four-digit room number."; // 重置房间号消息
        roomErrorMessage.classList.remove('text-danger'); // 移除错误样式
    }

    // 验证密码是否为四位数字
    if (!/^\d{4}$/.test(password)) {
        if (!roomErrorMessage.classList.contains('text-danger')) { // 只在房间号有效时显示密码错误
            passwordErrorMessage.textContent = "Please enter a valid four-digit password."; // 更新密码错误消息
            passwordErrorMessage.classList.add('text-danger'); // 添加错误样式
        }
    } else {
        passwordErrorMessage.textContent = ""; // 清空密码错误消息
        passwordErrorMessage.classList.remove('text-danger'); // 移除错误样式
    }

    // 如果两个输入都有效，则可以提交
    if (/^\d{4}$/.test(roomNumber) && /^\d{4}$/.test(password)) {
        // alert("Room number and password are valid!"); // 可以在这里处理表单提交
        this.submit(); // 如果要实际提交表单，可以取消注释这行
    }
});

document.getElementById('showPasswordCheck').addEventListener('change', function() {
    var passwordInput = document.getElementById('exampleInputPassword1');
    if (this.checked) {
        passwordInput.type = 'text'; // 显示密码
    } else {
        passwordInput.type = 'password'; // 隐藏密码
    }
});