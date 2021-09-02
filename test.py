# test code
# 代码测试

a = {'a':[1,2,3], 'b': [4,5,6]}
print(a.values())

delete_orders = [1,4, 2,3]

# 过期或者拒绝的订单删除掉.
for delete_order in delete_orders:
    for key in a:
        orders = a.get(key, [])
        if delete_order in orders:
            orders.remove(delete_order)
        a[key] = orders
print(a)
