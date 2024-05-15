case $1 in
    "run")
        python3.12 marketsvc/server.py
        ;;
    "customers")
        curl http://localhost:9090/api/customers
        ;;
    "custorders")
        curl http://localhost:9090/api/orders/${2:-1}
        ;;
    "ordertotal")
        curl http://localhost:9090/api/order_total/${2:-1}
        ;;
    "orderstotal")
        curl -X GET -H "Content-Type: application/json" -d '{"orders":[1,2,3,4,5,6,7,8,9,10]}' http://localhost:9090/api/orders_total
        ;;
    "ordersbet")
        curl "http://localhost:9090/api/orders_between_dates/2024-03-22/2024-03-14"
        ;;
    "neworder")
        curl -H "Content-Type: application/json" -d '{"customer_id":1,"items":[{"id":2,"quantity":4},{"id":3,"quantity":6}]}' http://localhost:9090/api/add_new_order
        ;;
    *)
        echo "unknown cmd: I know [run, customers, custorders, ordertotal, ordersbet, neworder, orderstotal]"
esac
