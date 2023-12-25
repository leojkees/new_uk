// function changeClass() {
//     var screenWidth = window.innerWidth;
//     var containElement = document.getElementById('contain');

//     if (screenWidth < 1200) {
//         containElement.classList.remove('col-10');
//         containElement.classList.add('col-12');
//     } else {
//         containElement.classList.remove('col-12');
//         containElement.classList.add('col-10');
//     }
// }

// // Вызываем функцию changeClass при загрузке страницы и при изменении размера окна
// window.addEventListener('load', changeClass);
// window.addEventListener('resize', changeClass);


// let lastScrollTop = 0;
// let menuDown = document.getElementById("menu-down");

// window.addEventListener("scroll", function() {
//     // Проверяем ширину экрана
//     if (window.innerWidth < 1024) {
//         let st = window.pageYOffset || document.documentElement.scrollTop;

//         // Определяем направление прокрутки
//         let scrollDirection = (st > lastScrollTop) ? 'up' : 'down';

//         // Рассчитываем изменение opacity на основе прокрутки
//         let opacityStepDown = 50; // Количество пикселей для изменения opacity при прокрутке вниз
//         let opacityStepUp = 10; // Количество пикселей для изменения opacity при прокрутке вверх

//         // Увеличиваем или уменьшаем opacity в зависимости от направления прокрутки
//         let opacity = (scrollDirection === 'down') ? st / opacityStepDown : 1 - (st / opacityStepUp);

//         // Ограничиваем значение opacity от 0 до 1
//         opacity = Math.min(1, Math.max(0, opacity));

//         // Присваиваем класс в зависимости от значения opacity
//         if (opacity >= 0.75) {
//             menuDown.className = "container fixed-bottom shadow p-3 bg-body rounded opacity-100";
//         } else if (opacity >= 0.5) {
//             menuDown.className = "container fixed-bottom shadow p-3 bg-body rounded opacity-75";
//         } else if (opacity >= 0.25) {
//             menuDown.className = "container fixed-bottom shadow p-3 bg-body rounded opacity-50";
//         } else if (opacity > 0) {
//             menuDown.className = "container fixed-bottom shadow p-3 bg-body rounded opacity-25";
//         } else {
//             menuDown.className = "container fixed-bottom shadow p-3 bg-body rounded opacity-0";
//         }

//         lastScrollTop = st <= 0 ? 0 : st; // Не учитывать прокрутку наверх за пределы страницы
//     }
// });

let lastScrollTop = 0;

window.addEventListener("scroll", function() {
    let st = window.pageYOffset || document.documentElement.scrollTop;
    let menuDown = document.getElementById("menu-down");

    if (window.innerWidth < 1024) {
        if (st > lastScrollTop) {
            // Прокрутка вниз
            menuDown.classList.add("d-none");
        } else {
            // Прокрутка вверх
            menuDown.classList.remove("d-none");
        }
    }

    lastScrollTop = st <= 0 ? 0 : st; // Не учитывать прокрутку наверх за пределы страницы
});



// var panel = document.getElementById('left-panel');

// document.addEventListener('scroll', function () {
//     var scrollY = window.scrollY || window.pageYOffset;

//     if (scrollY > 100) {
//         panel.style.top = scrollY - 200 + 'px';
//     } else {
//         panel.style.top = '100px';
//     }
// });
// var panel = document.getElementById('left-panel');
// var initialTop = 100;
// var scrollOffset = 200;

// document.addEventListener('scroll', function () {
//     var scrollY = window.scrollY || window.pageYOffset;

//     if (scrollY > initialTop) {
//         panel.style.transition = 'top 0.3s ease'; // Включаем плавный переход
//         panel.style.top = (scrollY - initialTop > scrollOffset) ? scrollOffset + 'px' : (scrollY - initialTop) + 'px';
//     } else {
//         panel.style.transition = 'top 0.3s ease'; // Включаем плавный переход
//         panel.style.top = initialTop + 'px';
//     }
// });
var panel = document.getElementById('left-panel');
var initialTop = 100;
var scrollThreshold = 300;
var isScrollingDown = true;

document.addEventListener('scroll', function () {
    var scrollY = window.scrollY || window.pageYOffset;

    if (scrollY > initialTop) {
        // Проверка направления прокрутки
        if (scrollY > initialTop + scrollThreshold && isScrollingDown) {
            isScrollingDown = false;
            panel.style.transition = 'top 0.3s ease';
            panel.style.top = '0';
        } else if (scrollY <= initialTop + scrollThreshold && !isScrollingDown) {
            isScrollingDown = true;
            panel.style.transition = 'top 0.3s ease';
            panel.style.top = initialTop + 'px';
        }
    } else {
        panel.style.transition = 'top 0.3s ease';
        panel.style.top = initialTop + 'px';
    }
});



var panel = document.getElementById('right-panel');
var initialTop = 100;
var scrollThreshold = 300;
var isScrollingDown = true;

document.addEventListener('scroll', function () {
    var scrollY = window.scrollY || window.pageYOffset;

    if (scrollY > initialTop) {
        // Проверка направления прокрутки
        if (scrollY > initialTop + scrollThreshold && isScrollingDown) {
            isScrollingDown = false;
            panel.style.transition = 'top 0.3s ease';
            panel.style.top = '0';
        } else if (scrollY <= initialTop + scrollThreshold && !isScrollingDown) {
            isScrollingDown = true;
            panel.style.transition = 'top 0.3s ease';
            panel.style.top = initialTop + 'px';
        }
    } else {
        panel.style.transition = 'top 0.3s ease';
        panel.style.top = initialTop + 'px';
    }
});


document.addEventListener("DOMContentLoaded", function() {
    var scrollToTopBtn = document.getElementById("scrollToTopBtn");
  
    // Показываем/скрываем кнопку при прокрутке
    window.onscroll = function() {
      if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        scrollToTopBtn.style.display = "block";
      } else {
        scrollToTopBtn.style.display = "none";
      }
    };
  
    // Прокрутка страницы вверх при клике на кнопку
    scrollToTopBtn.addEventListener("click", function() {
      document.body.scrollTop = 0; // Для Safari
      document.documentElement.scrollTop = 0; // Для остальных браузеров
    });
  });
  








