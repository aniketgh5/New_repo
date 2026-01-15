from flask import Flask, render_template_string, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

products = [
    {"id": 1, "name": "Wireless Headphones", "price": 99.99, "image": "https://picsum.photos/300/200?random=1", "category": "Electronics", "description": "High-quality wireless headphones with noise cancellation", "rating": 4.5},
    {"id": 2, "name": "Smart Watch", "price": 199.99, "image": "https://picsum.photos/300/200?random=2", "category": "Electronics", "description": "Feature-rich smartwatch with health monitoring", "rating": 4.2},
    {"id": 3, "name": "Running Shoes", "price": 79.99, "image": "https://picsum.photos/300/200?random=3", "category": "Fashion", "description": "Comfortable running shoes for all terrains", "rating": 4.7},
    {"id": 4, "name": "Coffee Maker", "price": 49.99, "image": "https://picsum.photos/300/200?random=4", "category": "Home", "description": "Automatic coffee maker with timer", "rating": 4.3},
    {"id": 5, "name": "Backpack", "price": 39.99, "image": "https://picsum.photos/300/200?random=5", "category": "Fashion", "description": "Waterproof backpack with laptop compartment", "rating": 4.6},
    {"id": 6, "name": "Desk Lamp", "price": 29.99, "image": "https://picsum.photos/300/200?random=6", "category": "Home", "description": "LED desk lamp with adjustable brightness", "rating": 4.4}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>ShopEasy</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>

<body class="bg-slate-100">

<!-- NAVBAR -->
<nav class="bg-slate-900 shadow sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <div class="flex items-center">
            <i class="fas fa-shopping-bag text-teal-400 text-2xl mr-2"></i>
            <span class="text-xl font-bold text-white">ShopEasy</span>
        </div>
        <button onclick="toggleCart()" class="relative text-slate-300 hover:text-teal-400">
            <i class="fas fa-shopping-cart text-xl"></i>
            <span id="cartCount" class="absolute -top-2 -right-2 bg-rose-500 text-white rounded-full text-xs w-5 h-5 flex items-center justify-center">0</span>
        </button>
    </div>
</nav>

<!-- HERO -->
<section class="bg-gradient-to-r from-teal-600 to-emerald-500 text-white py-16 text-center">
    <h1 class="text-5xl font-bold mb-4">Welcome to ShopEasy</h1>
    <p class="text-xl">Modern shopping made simple</p>
</section>

<!-- PRODUCTS -->
<section class="max-w-7xl mx-auto px-4 py-12">
    <h2 class="text-3xl font-bold text-center mb-8 text-slate-800">Featured Products</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {% for product in products %}
        <div class="bg-white rounded-lg shadow hover:-translate-y-1 transition">
            <img src="{{ product.image }}" class="rounded-t-lg h-48 w-full object-cover">
            <div class="p-4">
                <h3 class="font-semibold text-lg text-slate-800">{{ product.name }}</h3>
                <p class="text-slate-600 text-sm">{{ product.description }}</p>
                <div class="flex justify-between items-center mt-3">
                    <span class="text-emerald-600 font-bold">${{ product.price }}</span>
                    <button onclick="addToCart({{ product.id }})"
                        class="bg-teal-600 text-white px-4 py-2 rounded hover:bg-teal-700">
                        Add to Cart
                    </button>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</section>

<!-- CART -->
<div id="cartSidebar" class="fixed right-0 top-0 w-80 h-full bg-white shadow-xl transform translate-x-full transition z-50">
    <div class="p-4 border-b flex justify-between">
        <h3 class="font-bold">Cart</h3>
        <button onclick="toggleCart()">✖</button>
    </div>
    <div id="cartItems" class="p-4"></div>
</div>

<div id="overlay" onclick="toggleCart()" class="hidden fixed inset-0 bg-black bg-opacity-50 z-40"></div>

<!-- FOOTER -->
<footer class="bg-slate-900 text-slate-400 text-center py-6">
    © 2024 ShopEasy | Built with Flask
</footer>

<script>
let cart = [];

function toggleCart(){
    document.getElementById('cartSidebar').classList.toggle('translate-x-full');
    document.getElementById('overlay').classList.toggle('hidden');
}

function addToCart(id){
    fetch('/add_to_cart',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({product_id:id})})
    .then(res=>res.json()).then(data=>{
        cart=data.cart;
        updateCart();
        notify("Added to cart","success");
    });
}

function updateCart(){
    document.getElementById('cartCount').innerText = cart.reduce((a,b)=>a+b.quantity,0);
    document.getElementById('cartItems').innerHTML = cart.map(i=>`
        <div class="flex justify-between border-b py-2">
            <span>${i.name} x ${i.quantity}</span>
            <span>$${i.price}</span>
        </div>`).join('');
}

function notify(msg,type){
    let n=document.createElement('div');
    n.className=`fixed top-4 right-4 px-4 py-2 rounded text-white ${type==='success'?'bg-emerald-500':'bg-rose-500'}`;
    n.innerText=msg;
    document.body.appendChild(n);
    setTimeout(()=>n.remove(),3000);
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, products=products)

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = []
    pid = request.json['product_id']
    p = next(p for p in products if p['id']==pid)
    cart=session['cart']
    item=next((i for i in cart if i['id']==pid),None)
    if item: item['quantity']+=1
    else: cart.append({"id":p['id'],"name":p['name'],"price":p['price'],"quantity":1})
    session['cart']=cart
    return jsonify(success=True,cart=cart)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
