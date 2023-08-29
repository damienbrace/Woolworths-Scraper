text = "/shop/productdetails/298548/abe-s-bagels-brioche-bagels"

sku = (text.split('details/'))
sku = (sku[1].split('/')[0])
print(sku)