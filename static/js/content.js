function autoResizeParent() {
    const formfloating = document.querySelector('.form-floating');
    const formcontrol = document.querySelector('.form-control');
    
    formfloating.style.height = 'auto';
    formfloating.style.height = formcontrol.scrollHeight + 'px';
}

document.getElementById('fileUploadLink').addEventListener('click', function() {
    document.querySelector('.comments').style.display = 'none';
    document.querySelector('.record').style.display = 'none';
    document.querySelector('.file_upload').style.display = 'block';
});

document.getElementById('textButton').addEventListener('click', function() {
    document.querySelector('.comments').style.display = 'block';
    document.querySelector('.record').style.display = 'block'; // 或 'inline' 根据您的布局需求
    document.querySelector('.file_upload').style.display = 'none';
});

// document.getElementById('photoButton').addEventListener('click', function() {
//     document.querySelector('.comments').style.display = 'none';
//     document.querySelector('.record').style.display = 'none';
//     document.querySelector('.file_upload').style.display = 'none';
// });


function setActiveButton(activeButtonId) {
    // 移除所有按钮的 active 类和 text-white 类
    const buttons = document.querySelectorAll('.nav-link');
    buttons.forEach(button => {
        button.classList.remove('active');
        button.classList.add('text-white'); // 确保其他按钮有 text-white 类
    });

    // 为被点击的按钮添加 active 类并移除 text-white 类
    const activeButton = document.getElementById(activeButtonId);
    activeButton.classList.add('active');
    activeButton.classList.remove('text-white');
}

// 事件监听器
document.getElementById('textButton').addEventListener('click', function() {
    setActiveButton('textButton');
    // 其他逻辑
});

document.getElementById('fileUploadLink').addEventListener('click', function() {
    setActiveButton('fileUploadLink');
    // 其他逻辑
});

// document.getElementById('photoButton').addEventListener('click', function() {
//     setActiveButton('photoButton');
//     // 其他逻辑
// });

document.getElementById("fileInput").addEventListener("change", function() {
    const fileName = this.files[0] ? this.files[0].name : 'No file chosen';
    document.getElementById("fileName").textContent = fileName;
  });

document.getElementById("cancelButton").addEventListener("click", function() {
// 清除文件输入
document.getElementById("fileInput").value = "";
// 重置文件名称文本
document.getElementById("fileName").textContent = "No file chosen";
});


