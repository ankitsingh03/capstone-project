import React, { Component } from 'react';
import {connect} from 'react-redux'
import cart from '../store/cart';
class RazorPanel extends Component {
    constructor(props) {
        super(props)

    }

    

    RequestOrderPayment(cartTotal){
      var abc = {
        "amount": cartTotal,
        "currency": "INR",
        "receipt": "rcptid_11"
    }
    console.log(cartTotal, "helloo***************************")
      fetch('http://127.0.0.1:8000/api/payment/', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(abc)
        })
        .then(response => response.json())
        .then(data => {
          console.log(data)
          var options = {
            "key_id": "rzp_test_BXuuvSnv4i88g9",
            "key_secret": "UwnwdougBKgb4Z5Vl0zMiJq6",
            "amount": cartTotal*100,
            "currency": data.currency,
            "name": "Acme Corp",
            "description": "A Wild Sheep Chase is the third novel by Japanese author  Haruki Murakami",
            "order_id": data.id,
            "callback_url": "http://127.0.0.1:8000/api/payment_success/",
            "prefill": {
                "name": "Gaurav Kumar",
                "email": "gaurav.kumar@example.com",
                "contact": "9999999999",
            },
            "notes": {
                "address": "note value",
            },
            "theme": {
                "color": "#F37254"
            }
        };
        var rzp1 = new window.Razorpay(options);
        rzp1.open();
    }
        )}
                

    render() {
        
        const {cartTotal} = this.props
        console.log(cartTotal,"hiiii *******")


        return (
            <div>
                <button id="rzp-button1" onClick={() => this.RequestOrderPayment(cartTotal)}>Pay</button>
            </div>
        )
    }
}
const mapState = (state) => {
    return {
    //   cart: state.cart.myCart,
      cartTotal: state.cart.total,
    //   products: state.cartProducts
    }
}
export default connect(mapState)(RazorPanel)

// export default RazorPanel;