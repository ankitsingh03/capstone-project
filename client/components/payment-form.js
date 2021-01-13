import React, { Component } from 'react';
import { clearCart } from '../store'
import { connect } from 'react-redux'
import { browserHistory } from 'react-router';
import cart from '../store/cart';
import user from '../store/user';
class RazorPanel extends Component {
    constructor(props) {
        super(props)

    }

    RequestOrderPayment(cartTotal, checkout, cart) {
        var info = {
            "amount": cartTotal,
            "currency": "USD",
            "receipt": "rcptid_11",
        }
        fetch('http://127.0.0.1:8000/api/payment/', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(info)
        })
            .then(response => response.json())
            .then(data => {
                var options = {
                    "key_id": "rzp_test_BXuuvSnv4i88g9",
                    "key_secret": "UwnwdougBKgb4Z5Vl0zMiJq6",
                    "amount": cartTotal * 100,
                    "currency": data.currency,
                    "name": "Smart Mart",
                    "order_id": data.id,
                    handler(response) {
                        var body = {
                            "payment_id": response.razorpay_payment_id,
                            "order_id": response.razorpay_order_id,
                            "signature": response.razorpay_signature,
                            "amount": cartTotal * 100,
                            "currency": data.currency,
                            "cart": cart,
                            "checkout":checkout
                        }
                        fetch('http://127.0.0.1:8000/api/payment_success', {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify(body)
                        })
                    },
                    "prefill": {
                        "name": checkout.firstname,
                        "email": checkout.email,
                        "contact": checkout.phone,
                    },
                    "theme": {
                        "color": "#F37254"
                    }
                };
                var rzp1 = new Razorpay(options);
                rzp1.on('payment.failed', function (response) {
                    alert(response.error.description);
                });
                rzp1.open();
            }
            )
    }

    render() {

        const { cartTotal, cart, checkout, user } = this.props
        return (

            <div>
                {
                    
                    user.id
                ?<button id="rzp-button1" onClick={() => {this.RequestOrderPayment(cartTotal, checkout, cart); clearCart();}}>Pay</button> 
                :<p>Please Login To proceed to Order</p>
                }
            </div>
        )
    }
}
const mapState = (state) => {
    return {
        user: state.user,
        cart: state.cart.myCart,
        cartTotal: state.cart.total,
        checkout: state.checkout

    }
}
export default connect(mapState)(RazorPanel)

// export default RazorPanel;