import React, { Component } from 'react';

class RazorPanel extends Component {
    constructor(props) {
        super(props)

    }
    

    RequestOrderPayment(){
      var abc = {
        "amount": 50000,
        "currency": "INR",
        "receipt": "rcptid_11"
    }
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
            "amount": data.amount*100,
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
        return (
            <div>
                <button id="rzp-button1" onClick={() => this.RequestOrderPayment()}>Pay</button>
            </div>
        )
    }
}
export default RazorPanel;