// Kategori menü pencere ayarı başı
var kategoriItemElement = document.querySelector('.kategori-item');
var altKategoriMenuElement = document.querySelector('.alt-kategori-menu');
function showAltKategoriMenu() {
  altKategoriMenuElement.style.display = 'block';
}

function hideAltKategoriMenu() {
  altKategoriMenuElement.style.display = 'none';
}

// sidebar kategori ayar başı
kategoriItemElement.addEventListener('mouseover', showAltKategoriMenu);
kategoriItemElement.addEventListener('mouseout', hideAltKategoriMenu);
// kategori menü pencere ayarı sonu


var toggleButtons = document.querySelectorAll('.toggle-button');

toggleButtons.forEach(function(button) {
  button.addEventListener('click', function() {
    this.classList.toggle('active');
    var panelCollapse = this.parentElement.nextElementSibling;
    panelCollapse.classList.toggle('show');
  });
});

var menuButton = document.querySelector('.menu_ac');
var sidebar = document.querySelector('#pencere');
var closeSidebarButton = document.querySelector('.sidebar_kapat');
function openSidebar() {
  sidebar.style.display = 'block';
}
function closeSidebar() {
  sidebar.style.display = 'none';
}
menuButton.addEventListener('click', openSidebar);
closeSidebarButton.addEventListener('click', closeSidebar);
// sidebar kategori ayar sonu



// Kaç tane resim varsa o kadar carousel indicator butonu olsun ayar başı
window.addEventListener('DOMContentLoaded', function() {
  var productCards = document.querySelectorAll('.card.product');
  productCards.forEach(function(card, index) {
    var carouselIndicatorsContainer = card.querySelector('.carousel-indicators');
    var carouselItems = card.querySelectorAll('.carousel-inner .carousel-item');
    
    carouselIndicatorsContainer.innerHTML = ''; 
    
    carouselItems.forEach(function(item, itemIndex) {
      var indicator = document.createElement('button');
      indicator.setAttribute('type', 'button');
      indicator.style.backgroundColor = '#333';
      indicator.setAttribute('data-bs-target', '#carouselExampleIndicators' + (index + 1));
      indicator.setAttribute('data-bs-slide-to', itemIndex.toString());
      indicator.setAttribute('aria-label', 'Slide ' + (itemIndex + 1).toString());
      
      if (itemIndex === 0) {
        indicator.classList.add('active');
        indicator.setAttribute('aria-current', 'true');
      }
      
      carouselIndicatorsContainer.appendChild(indicator);
    });
  });
});
// Kaç tane resim varsa o kadar carousel indicator butonu olsun ayar başı


var favoriButtons = document.querySelectorAll('.favori');

favoriButtons.forEach(function(button) {
  button.addEventListener('mouseover', function() {
    var heartIcon = button.querySelector('.fa-regular.fa-heart');
    heartIcon.style.color = '#ff0000';
  });

  button.addEventListener('mouseout', function() {
    var heartIcon = button.querySelector('.fa-regular.fa-heart');
    heartIcon.style.color = '#919193';
  });
});
  // favori butonu ayarı sonu





