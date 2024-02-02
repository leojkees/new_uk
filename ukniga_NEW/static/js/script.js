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












// var panel = document.getElementById('left-panel');
// var initialTop = 100;
// var scrollThreshold = 300;
// var isScrollingDown = true;

// document.addEventListener('scroll', function () {
//     var scrollY = window.scrollY || window.pageYOffset;

//     if (scrollY > initialTop) {
//         // Проверка направления прокрутки
//         if (scrollY > initialTop + scrollThreshold && isScrollingDown) {
//             isScrollingDown = false;
//             panel.style.transition = 'top 0.3s ease';
//             panel.style.top = '0';
//         } else if (scrollY <= initialTop + scrollThreshold && !isScrollingDown) {
//             isScrollingDown = true;
//             panel.style.transition = 'top 0.3s ease';
//             panel.style.top = initialTop + 'px';
//         }
//     } else {
//         panel.style.transition = 'top 0.3s ease';
//         panel.style.top = initialTop + 'px';
//     }
// });



// var panel = document.getElementById('right-panel');
// var initialTop = 100;
// var scrollThreshold = 300;
// var isScrollingDown = true;

// document.addEventListener('scroll', function () {
//     var scrollY = window.scrollY || window.pageYOffset;

//     if (scrollY > initialTop) {
//         // Проверка направления прокрутки
//         if (scrollY > initialTop + scrollThreshold && isScrollingDown) {
//             isScrollingDown = false;
//             panel.style.transition = 'top 0.3s ease';
//             panel.style.top = '0';
//         } else if (scrollY <= initialTop + scrollThreshold && !isScrollingDown) {
//             isScrollingDown = true;
//             panel.style.transition = 'top 0.3s ease';
//             panel.style.top = initialTop + 'px';
//         }
//     } else {
//         panel.style.transition = 'top 0.3s ease';
//         panel.style.top = initialTop + 'px';
//     }
// });

// //скролл бокового меню
// document.addEventListener("DOMContentLoaded", function() {
//     var scrollToTopBtn = document.getElementById("scrollToTopBtn");
  
//     // Показываем/скрываем кнопку при прокрутке
//     window.onscroll = function() {
//       if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
//         scrollToTopBtn.style.display = "block";
//       } else {
//         scrollToTopBtn.style.display = "none";
//       }
//     };
  
//     // Прокрутка страницы вверх при клике на кнопку
//     scrollToTopBtn.addEventListener("click", function() {
//       document.body.scrollTop = 0; // Для Safari
//       document.documentElement.scrollTop = 0; // Для остальных браузеров
//     });
//   });
  


// const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
// const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));




// //подгонка под экраны мака
// function updateClass(elementId) {
//     var element = document.getElementById(elementId);

//     if (element) {
//       if (window.innerWidth >= 340 && window.innerWidth <= 1586) {
//         element.className = "col-12";
//       } else if (window.innerWidth > 1586 && window.innerWidth <= 1810) {
//         element.className = "col-10";
//       } else if (window.innerWidth > 1810 && window.innerWidth <= 3440) {
//         element.className = "col-12";
//       }
//     }
//   }

//   // Вызывается при загрузке страницы и изменении размера окна
//   window.onload = function() {
//     updateClass("content");
//     updateClass("brcr");
//     updateClass("dwnm");
// };

//   window.onresize = function() {
//     updateClass("content");
//     updateClass("brcr");
//     updateClass("dwnm");
// };

// JavaScript для прокрутки ленты влево и вправо
// document.addEventListener("DOMContentLoaded", function() {
//   const cardContainer = document.querySelector('.card-container');
//   const cardWidth = cardContainer.clientWidth / 3; // Получаем ширину одной карточки
//   const prevBtn = document.querySelector('.prev-btn');
//   const nextBtn = document.querySelector('.next-btn');

//   // Функция для прокрутки влево
//   prevBtn.addEventListener('click', function() {
//       cardContainer.scrollBy({
//           left: -cardWidth,
//           behavior: 'smooth'
//       });
//   });

//   // Функция для прокрутки вправо
//   nextBtn.addEventListener('click', function() {
//       cardContainer.scrollBy({
//           left: cardWidth,
//           behavior: 'smooth'
//       });
//   });
// });
// document.addEventListener("DOMContentLoaded", function() {
//   function setupCardScroll(containerId, prevBtnId, nextBtnId) {
//     const cardContainer = document.getElementById(containerId);
//     const prevBtn = document.getElementById(prevBtnId);
//     const nextBtn = document.getElementById(nextBtnId);

//     if (!cardContainer || !prevBtn || !nextBtn) {
//       console.error('Не удалось найти контейнер или кнопки.');
//       return;
//     }

//     // Получаем ширину одной карточки
//     const firstCard = cardContainer.querySelector('.card');
//     const cardWidth = firstCard.offsetWidth + 8; // добавляем 8 пикселей

//     // Функция для прокрутки влево
//     prevBtn.addEventListener('click', function() {
//       cardContainer.scrollBy({
//         left: -cardWidth,
//         behavior: 'smooth'
//       });
//     });

//     // Функция для прокрутки вправо
//     nextBtn.addEventListener('click', function() {
//       cardContainer.scrollBy({
//         left: cardWidth,
//         behavior: 'smooth'
//       });
//     });
//   }

//   // Настройка для блока с id="index"
//   setupCardScroll('index', 'prev-btn-index', 'next-btn-index');

//   // Настройка для блока с id="index"
//   setupCardScroll('bookrinok', 'prev-btn-bookrinok', 'next-btn-bookrinok');
  
//   // Настройка для блока с id="interview"
//   setupCardScroll('interview', 'prev-btn-interview', 'next-btn-interview');
// });
document.addEventListener("DOMContentLoaded", function() {
  function setupCardScroll(containerId, prevBtnId, nextBtnId) {
    const cardContainer = document.getElementById(containerId);
    const prevBtn = document.getElementById(prevBtnId);
    const nextBtn = document.getElementById(nextBtnId);

    if (!cardContainer || !prevBtn || !nextBtn) {
      console.error('Не удалось найти контейнер или кнопки.');
      return;
    }

    // Получаем ширину одной карточки
    const firstCard = cardContainer.querySelector('.card');
    const cardWidth = firstCard.offsetWidth + 8; // добавляем 8 пикселей

    // Для хранения начальной позиции касания
    let touchStartX = 0;

    // Функция для обработки события начала касания
    function onTouchStart(event) {
      touchStartX = event.touches[0].clientX;
    }

    // Функция для обработки события окончания касания
    function onTouchEnd(event) {
      const touchEndX = event.changedTouches[0].clientX;
      const deltaX = touchEndX - touchStartX;

      if (deltaX > 50) {
        // Свайп вправо, прокручиваем влево
        cardContainer.scrollBy({
          left: -cardWidth,
          behavior: 'smooth'
        });
      } else if (deltaX < -50) {
        // Свайп влево, прокручиваем вправо
        cardContainer.scrollBy({
          left: cardWidth,
          behavior: 'smooth'
        });
      }
    }

    // Добавляем обработчики событий касания
    cardContainer.addEventListener('touchstart', onTouchStart);
    cardContainer.addEventListener('touchend', onTouchEnd);

    // Функция для прокрутки влево
    prevBtn.addEventListener('click', function() {
      cardContainer.scrollBy({
        left: -cardWidth,
        behavior: 'smooth'
      });
    });

    // Функция для прокрутки вправо
    nextBtn.addEventListener('click', function() {
      cardContainer.scrollBy({
        left: cardWidth,
        behavior: 'smooth'
      });
    });
  }

  // Настройка для блока с id="index"
  setupCardScroll('index', 'prev-btn-index', 'next-btn-index');

  // Настройка для блока с id="bookrinok"
  setupCardScroll('bookrinok', 'prev-btn-bookrinok', 'next-btn-bookrinok');

  // Настройка для блока с id="ostraya"
  setupCardScroll('ostraya', 'prev-btn-ostraya', 'next-btn-ostraya');

  // Настройка для блока с id="vistavki"
  setupCardScroll('vistavki', 'prev-btn-vistavki', 'next-btn-vistavki');

  // Настройка для блока с id="biblioteki"
  setupCardScroll('biblioteki', 'prev-btn-biblioteki', 'next-btn-biblioteki');

  // Настройка для блока с id="nauka"
  setupCardScroll('nauka', 'prev-btn-nauka', 'next-btn-nauka');
  
  // Настройка для блока с id="inovations"
  setupCardScroll('inovations', 'prev-btn-inovations', 'next-btn-inovations');

  // Настройка для блока с id="сreative"
  setupCardScroll('сreative', 'prev-btn-сreative', 'next-btn-сreative');
  
  // Настройка для блока с id="interview"
  setupCardScroll('interview', 'prev-btn-interview', 'next-btn-interview');
});




const panel = document.getElementById('left-menu');
const speedFactor = -0.8; // Отрицательная скорость прокрутки панели

window.addEventListener('scroll', function() {
  const offset = window.pageYOffset * speedFactor;
  panel.style.transform = 'translateY(' + offset + 'px)';
});
