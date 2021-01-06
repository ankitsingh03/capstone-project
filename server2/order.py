import razorpay

client = razorpay.Client(auth=("rzp_test_BXuuvSnv4i88g9","UwnwdougBKgb4Z5Vl0zMiJq6"))
order_amount = 10000 #request.data['amount']
order_currency = 'INR'
order_receipt = 'order_rct_1'
response = client.order.create(dict(amount=order_amount,
                    currency=order_currency,
                    receipt = order_receipt))
print(response)
order_id = response['id']
print(order_id)