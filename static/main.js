// A list of my products in arrays
const Items = [
  {
    name: 'Headwrap & Earrings',
    price: 100.0,
    quantity: 0,
  },

  {
    name: 'Men Mbhaco Pants',
    price: 100.00,
    quantity: 0,
  },
  {
    name: 'Skirt & Scarf & Headwrap',
    price: 400.00,
    quantity: 0,
  },

  {
    name: "Men's 3pc attire",
    price: 400.00,
    quantity: 0,
  },

  {
    name: 'Modern Mbhaco Dress',
    price: 300.00,
    quantity: 0,
  },

  {
    name: 'Indlovukazi Dress',
    price: 2500.00,
    quantity: 0,
  },

  {
    name: "Men's Black & White 3pc",
    price: 600.00,
    quantity: 0,
  },

  {
    name: 'Modern Ball Gown ',
    price: 2000.00,
    quantity: 0,
  },

  {
    name: 'Elegant New pattern',
    price: 1000.00,
    quantity: 0,
  },

  {
    name: "King's 2pc",
    price: 300.00,
    quantity: 0,
  },

  {
    name: "Queen's 2pc Dress",
    price: 2000.00,
    quantity: 0,
  },

  {
    name: 'Unisex Scarf',
    price: 200.00,
    quantity: 0,
  },
];

// targeting all products that can be added to the cart
let shoppingCart = document.querySelectorAll('.add-btn');

// Loops through the cart items
for (let i = 0; i < shoppingCart.length; i++) {
  // adding a onclick to all the add to cart buttons
  shoppingCart[i].addEventListener('click', () => {
    // calling the function inside the loop
    cartProducts(Items[i]);
    calculateTotal(Items[i]);
  });
}

// saving items to the localStorage
const cartProducts = (Product) => {
  // getting the items from the localStorage
  let item = localStorage.getItem('cartProducts');

  //converting the itemid from a string to an interger
  item = parseInt(item);

  //checks if there are items in the local
  if (item) {
    //setting a product id for each cart item
    //if there are items into the cart already, they will be added ontop of the ones that exist in the cart
    localStorage.setItem('cartProducts', item + 1);
    //increases the cart-total GUI as items are added to the cart
    document.getElementById('cart-total').textContent = item + 1;
  } else {
    // if cart is equal to 0 then when add button is clicked, 1 will be displayed
    localStorage.setItem('cartProducts', 1);
    document.getElementById('cart-total').textContent = 1;
  }
  // calling the setItems function
  setItems(Product);
};

// checks for items inside the cart
const setItems = (Product) => {
  //checks if an item already exists in the cart and prevents it from being overwritten
  let cartItems = localStorage.getItem('productsCart');

  //convert cartItems from string to javascript
  cartItems = JSON.parse(cartItems);

  //if item exists in the cart add onto the existing one
  if (cartItems != null) {
    if (cartItems[Product.name] == undefined) {
      // Get the rest of the items that are in the cart using the rest operator
      cartItems = {
        ...cartItems,
        [Product.name]: Product,
      };
    }
    // adds a new item ontop of the one thats in the cart
    cartItems[Product.name].quantity += 1;
  } else {
    // records the items added to the cart and increments them
    Product.quantity = 1;
    // an object to save the products added to cart to the localStorage
    cartItems = {
      [Product.name]: Product,
    };
  }
  // converts items/products into a string and sets items into the localSorage
  localStorage.setItem('productsCart', JSON.stringify(cartItems));
};

//Calculates the total of the items in my cart
const calculateTotal = (Product) => {
  let cart_total = localStorage.getItem('calculateTotal');

  // if there are items in the cart, they will sum up together to calculate the total
  if (cart_total != null) {
    // changing the cart-total from a string to an interger in order to calculate the total
    cart_total = parseInt(cart_total);
    localStorage.setItem('calculateTotal', cart_total + Product.price);
  } else {
    localStorage.setItem('calculateTotal', Product.price);
  }
};

// this function will keep the items in the cart even if the page is reloaded
const keepItemsOnbrowser = () => {
  // getting the items from the localStorage
  let item = localStorage.getItem('cartProducts');

  //converting the item from a string to an interger
  item = parseInt(item);

  // displays the total of items in the local storage to the cart-total on the screen
  if (item) {
    document.getElementById('cart-total').textContent = item;
  }
};

// displaying the cart items from the localStorage to the cart.html
const displayItems = () => {
  // fetching the items from the local storage
  let cartItems = localStorage.getItem('productsCart');
  cartItems = JSON.parse(cartItems);
  

  let productsCart = document.querySelector('.products');
  
  if (cartItems && productsCart) {
    productsCart.innerHTML = '';
    Object.values(cartItems).map((item) => {
      productsCart.innerHTML += `
            <div class="products">
            <tbody>
              <td><small>${item.name}</small></td>
              <td><small>${item.quantity}</small></td>
              <td><small>R${item.price},00</small></td>
              </tbody>
            <div>   
            `;
    });

    let cartTotal = document.querySelector('.total');
    let cart_total = localStorage.getItem('calculateTotal');
    let item = localStorage.getItem('cartProducts');
    if (cartItems && cartTotal) {
      cartTotal.innerHTML = '';
      
        cartTotal.innerHTML += `
        <div class="total">
        <tr>
              <th>
                <h5>Items: <strong>${item}</strong></h5>
              </th>

              <th>
                <h5>Total: <strong>R${cart_total}</strong></h5>
              </th>
          </tr>
        </div>
        `
    
    }
  }
};

// removes items from cart after payment and reloads the page
const removeFromCart = () => {
  let item = localStorage.clear();
  // reloads page
  location.reload();
};

// creates an alert after form data is submitted
const payment = () => {
  alert("A Payment of R" + localStorage.getItem('calculateTotal') + " has been Completed! Thanks For shopping with Mbhaco Designs!");
// clears cart after the purchase
  let item = localStorage.clear();
  //location.reload();
}

// calling the function
keepItemsOnbrowser();
displayItems();
