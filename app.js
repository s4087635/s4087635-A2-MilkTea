const API_BASE_URL = "https://j2s64fo4qj.execute-api.us-east-1.amazonaws.com/prod";

let products = [];
let cart = [];

async function loadProducts() {
    try {
        const response = await fetch(`${API_BASE_URL}/products`);

        if (!response.ok) {
            throw new Error("Could not load products");
        }

        products = await response.json();

        displayProducts(products);

    } catch (error) {
        console.error("Error loading products:", error);

        document.getElementById("productGrid").innerHTML =
            "<p>Unable to load products. Please try again later.</p>";
    }
}

const productGrid =
    document.getElementById("productGrid");

const searchInput =
    document.getElementById("searchInput");

const categoryFilter =
    document.getElementById("categoryFilter");


function displayProducts(productList) {

    productGrid.innerHTML = "";

    productList.forEach(product => {

        const card = document.createElement("div");
        card.className = "product-card";

        card.innerHTML = `
            <img
                src="${product.image}"
                alt="${product.name}"
            >

            <div class="product-info">

                <h3>${product.name}</h3>

                <p class="category">
                    ${product.category}
                </p>

                <p class="description">
                    ${product.description}
                </p>

                <p class="price">
                    $${product.price.toFixed(2)}
                </p>

                <button
                    onclick="addToCart('${product.productId}')"
                >
                    Add to Order
                </button>

            </div>
        `;

        productGrid.appendChild(card);
    });
}


function filterProducts() {

    const search =
        searchInput.value.toLowerCase();

    const category =
        categoryFilter.value;

    const filtered =
        products.filter(product => {

            const matchesSearch =
                product.name
                    .toLowerCase()
                    .includes(search);

            const matchesCategory =
                category === "All" ||
                product.category === category;

            return matchesSearch && matchesCategory;
        });

    displayProducts(filtered);
}


searchInput.addEventListener(
    "input",
    filterProducts
);

categoryFilter.addEventListener(
    "change",
    filterProducts
);


function addToCart(productId) {

    const product =
        products.find(
            p => p.productId === productId
        );

    const existing =
        cart.find(
            item => item.productId === productId
        );

    if (existing) {
        existing.quantity++;
    } else {
        cart.push({
            ...product,
            quantity: 1
        });
    }

    displayCart();
}


function displayCart() {

    const cartItems =
        document.getElementById("cartItems");

    const totalPrice =
        document.getElementById("totalPrice");

    if (cart.length === 0) {

        cartItems.innerHTML =
            "<p>Your order is empty.</p>";

        totalPrice.textContent = "0.00";

        return;
    }

    cartItems.innerHTML = "";

    let total = 0;

    cart.forEach(item => {

        total += item.price * item.quantity;

        const row =
            document.createElement("div");

        row.className = "cart-row";

        row.innerHTML = `
            <span>
                ${item.name}
            </span>

            <span>
                Qty:
                <input
                    type="number"
                    min="1"
                    value="${item.quantity}"
                    onchange="
                        updateQuantity(
                            '${item.productId}',
                            this.value
                        )
                    "
                >
            </span>

            <span>
                $${(
                item.price *
                item.quantity
            ).toFixed(2)}
            </span>
        `;

        cartItems.appendChild(row);
    });

    totalPrice.textContent =
        total.toFixed(2);
}


function updateQuantity(
    productId,
    quantity
) {

    const item =
        cart.find(
            p => p.productId === productId
        );

    item.quantity =
        Math.max(
            1,
            parseInt(quantity)
        );

    displayCart();
}


document
    .getElementById("orderForm")
    .addEventListener(
        "submit",
        function (event) {

            event.preventDefault();

            const name =
                document
                    .getElementById(
                        "customerName"
                    )
                    .value.trim();

            const email =
                document
                    .getElementById(
                        "customerEmail"
                    )
                    .value.trim();

            const message =
                document
                    .getElementById(
                        "orderMessage"
                    );

            if (cart.length === 0) {

                message.textContent =
                    "Please add at least one drink.";

                message.style.color = "red";

                return;
            }

            if (!name || !email) {

                message.textContent =
                    "Please enter your name and email.";

                message.style.color = "red";

                return;
            }

            const order = {
                customerName: name,
                customerEmail: email,

                items: cart.map(item => ({
                    productId:
                        item.productId,

                    productName:
                        item.name,

                    quantity:
                        item.quantity,

                    price:
                        item.price
                })),

                totalAmount:
                    Number(
                        document
                            .getElementById(
                                "totalPrice"
                            )
                            .textContent
                    )
            };

            console.log(
                "Order submitted:",
                order
            );

            message.textContent =
                "Order request created successfully.";

            message.style.color = "green";

            /*
              Task F API gateway
            */
        }
    );


loadProducts();