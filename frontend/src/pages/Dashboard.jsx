import { useEffect, useState } from "react";
import api from "../services/api";

function Dashboard() {
  const [stats, setStats] = useState({
    total_products: 0,
    total_customers: 0,
    total_orders: 0,
    low_stock_products: 0,
  });

  const [products, setProducts] = useState([]);

  useEffect(() => {
    loadDashboard();
    loadProducts();
  }, []);

  const loadDashboard = async () => {
    try {
      const res = await api.get("/dashboard");
      setStats(res.data);
    } catch (error) {
      console.error(error);
    }
  };

  const loadProducts = async () => {
    try {
      const res = await api.get("/products");
      setProducts(res.data);
    } catch (error) {
      console.error(error);
    }
  };

  const lowStockProducts = products.filter(
    (product) => product.quantity < 5
  );

  return (
    <div>
      <h1>Dashboard</h1>

      <div className="cards">
        <div className="card">
          <h3>Total Products</h3>
          <p>{stats.total_products}</p>
        </div>

        <div className="card">
          <h3>Total Customers</h3>
          <p>{stats.total_customers}</p>
        </div>

        <div className="card">
          <h3>Total Orders</h3>
          <p>{stats.total_orders}</p>
        </div>

        <div className="card">
          <h3>Low Stock Products</h3>
          <p>{stats.low_stock_products}</p>
        </div>
      </div>

      <div
        style={{
          marginTop: "40px",
        }}
      >
        <h2>Low Stock Products</h2>

        <table
          style={{
            width: "100%",
            marginTop: "20px",
            background: "white",
          }}
        >
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>SKU</th>
              <th>Stock</th>
            </tr>
          </thead>

          <tbody>
            {lowStockProducts.map((product) => (
              <tr key={product.id}>
                <td>{product.id}</td>
                <td>{product.name}</td>
                <td>{product.sku}</td>
                <td>{product.quantity}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Dashboard;