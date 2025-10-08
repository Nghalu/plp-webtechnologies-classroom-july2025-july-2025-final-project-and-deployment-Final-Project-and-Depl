function filterProducts(category) {
    const products = document.querySelectorAll('.product');
    products.forEach(product => {
        product.style.display = product.dataset.category === category ? 'block' : 'none';
    });
}
