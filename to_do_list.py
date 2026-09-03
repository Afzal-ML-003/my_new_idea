import streamlit as st
import json
import os
from datetime import date

st.title("THIS IS MY 1st TO DO LIST IN STREAMLIT!")
st.header("\nThats Great Idea!")

DATA_FILE = "clients_data.json"


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4, default=str)


if "clients" not in st.session_state:
    st.session_state.clients = load_data()

if "selected_client" not in st.session_state:
    st.session_state.selected_client = None


with st.sidebar:
    st.title("LIST OF ITEMS")

    st.subheader("Naya Client Add Karein")
    new_client = st.text_input("Client ka naam likhein")
    if st.button("Add Client"):
        if new_client.strip() == "":
            st.warning("Pehle client ka naam likhein.")
        elif new_client in st.session_state.clients:
            st.warning("Ye client pehle se maujood hai.")
        else:
            st.session_state.clients[new_client] = {
                "mobile": "",
                "orders": []
            }
            save_data(st.session_state.clients)
            st.session_state.selected_client = new_client
            st.rerun()

    st.divider()
    st.subheader("Clients")

    if len(st.session_state.clients) == 0:
        st.write("Abhi koi client nahi hai.")
    else:
        for client_name in st.session_state.clients.keys():
            if st.button(client_name, key=f"btn_{client_name}"):
                st.session_state.selected_client = client_name
                st.rerun()


if st.session_state.selected_client is None:
    st.write("Sidebar se koi client select karein ya naya client add karein.")
else:
    client_name = st.session_state.selected_client
    client_data = st.session_state.clients[client_name]

    st.header(f"Client: {client_name}")

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Client Delete Karein"):
            del st.session_state.clients[client_name]
            save_data(st.session_state.clients)
            st.session_state.selected_client = None
            st.rerun()

    client_data["mobile"] = st.text_input(
        "Mobile Number", value=client_data.get("mobile", "")
    )

    st.subheader("Naya Order / Kaam Add Karein")
    with st.form(key=f"order_form_{client_name}", clear_on_submit=True):
        item = st.text_input("Item / Kaam ka naam")
        quantity = st.number_input("Quantity", min_value=0, step=1)
        price = st.number_input("Fi Item Qeemat (Rs)", min_value=0.0, step=1.0)
        order_date = st.date_input("Order Date", value=date.today())
        delivery_date = st.date_input("Delivery Date", value=date.today())
        description = st.text_area("Description")
        paid_amount = st.number_input("Kitna Payment Mila (Rs)", min_value=0.0, step=1.0)

        submitted = st.form_submit_button("Order Save Karein")
        if submitted:
            if item.strip() == "":
                st.warning("Item ka naam likhein.")
            else:
                total_price = quantity * price
                due_amount = total_price - paid_amount
                client_data["orders"].append({
                    "item": item,
                    "quantity": quantity,
                    "price": price,
                    "total_price": total_price,
                    "order_date": str(order_date),
                    "delivery_date": str(delivery_date),
                    "description": description,
                    "paid_amount": paid_amount,
                    "due_amount": due_amount,
                })
                save_data(st.session_state.clients)
                st.success("Order save ho gaya!")
                st.rerun()

    st.subheader("Client ke Sare Orders")
    if len(client_data["orders"]) == 0:
        st.write("Abhi koi order nahi hai.")
    else:
        total_business = 0
        total_paid = 0
        total_due = 0

        for idx, order in enumerate(client_data["orders"]):
            with st.expander(f"{order['item']} — {order['order_date']}"):
                st.write(f"**Quantity:** {order['quantity']}")
                st.write(f"**Fi Item Qeemat:** Rs {order['price']}")
                st.write(f"**Total Qeemat:** Rs {order['total_price']}")
                st.write(f"**Order Date:** {order['order_date']}")
                st.write(f"**Delivery Date:** {order['delivery_date']}")
                st.write(f"**Description:** {order['description']}")
                st.write(f"**Payment Mila:** Rs {order['paid_amount']}")
                st.write(f"**Baqi Payment:** Rs {order['due_amount']}")

                if st.button("Ye Order Delete Karein", key=f"del_{client_name}_{idx}"):
                    client_data["orders"].pop(idx)
                    save_data(st.session_state.clients)
                    st.rerun()

            total_business += order["total_price"]
            total_paid += order["paid_amount"]
            total_due += order["due_amount"]

        st.divider()
        st.subheader("Client ka Kul Hisaab")
        st.write(f"**Kul Business:** Rs {total_business}")
        st.write(f"**Kul Wasool Payment:** Rs {total_paid}")
        st.write(f"**Kul Baqi Payment:** Rs {total_due}")

    save_data(st.session_state.clients)

