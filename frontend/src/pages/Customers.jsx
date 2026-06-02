import { useEffect, useState } from "react";
import api from "../services/api";

function Customers() {
  const [customers, setCustomers] = useState([]);

  const [formData, setFormData] = useState({
    full_name: "",
    email: "",
    phone: "",
  });

  const [message, setMessage] = useState("");

  useEffect(() => {
    loadCustomers();
  }, []);

  const loadCustomers = async () => {
    try {
      const response = await api.get("/customers");
      setCustomers(response.data);
    } catch (error) {
      console.error(error);
      setMessage("Failed to load customers");
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const addCustomer = async (e) => {
    e.preventDefault();

    try {
      await api.post("/customers", formData);

      setMessage("Customer added successfully");

      setFormData({
        full_name: "",
        email: "",
        phone: "",
      });

      loadCustomers();
    } catch (error) {
      console.error(error);

      if (error.response?.data?.detail) {
        setMessage(error.response.data.detail);
      } else {
        setMessage("Failed to add customer");
      }
    }
  };

  const deleteCustomer = async (id) => {
    if (!window.confirm("Delete this customer?")) {
      return;
    }

    try {
      await api.delete(`/customers/${id}`);

      setMessage("Customer deleted successfully");

      loadCustomers();
    } catch (error) {
      console.error(error);
      setMessage("Failed to delete customer");
    }
  };

  return (
    <div>
      <h1>Customers</h1>

      {message && (
        <div
          style={{
            marginTop: "15px",
            marginBottom: "15px",
            padding: "10px",
            background: "#e2e8f0",
            borderRadius: "8px",
          }}
        >
          {message}
        </div>
      )}

      <form
        onSubmit={addCustomer}
        style={{
          display: "grid",
          gap: "12px",
          marginTop: "20px",
          marginBottom: "30px",
          maxWidth: "500px",
        }}
      >
        <input
          type="text"
          name="full_name"
          placeholder="Full Name"
          value={formData.full_name}
          onChange={handleChange}
          required
        />

        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />

        <input
          type="text"
          name="phone"
          placeholder="Phone Number"
          value={formData.phone}
          onChange={handleChange}
          required
        />

        <button type="submit">
          Add Customer
        </button>
      </form>

      <table
        style={{
          width: "100%",
          background: "white",
          borderCollapse: "collapse",
        }}
      >
        <thead>
          <tr>
            <th>ID</th>
            <th>Full Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          {customers.map((customer) => (
            <tr key={customer.id}>
              <td>{customer.id}</td>
              <td>{customer.full_name}</td>
              <td>{customer.email}</td>
              <td>{customer.phone}</td>

              <td>
                <button
                  onClick={() =>
                    deleteCustomer(customer.id)
                  }
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Customers;