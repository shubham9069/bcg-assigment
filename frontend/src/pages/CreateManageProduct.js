import React, { useState, useEffect } from "react";
import { Button, TextField, Select, MenuItem, Switch, FormControlLabel, Checkbox } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import Modal from "react-modal";
import ProductTable from "../components/ProductTable/ProductTable";
import Header from "../components/Header/Header";
import DemandForecastModal from "../components/DemandForecastModal/DemandForecastModal";
import axios from "axios";
import { useAuth } from "../context/AuthContext";
import { BASE_URL } from "../config";

const CreateManageProduct = () => {
  const { token } = useAuth();
  const [isAddModalOpen, setAddModalOpen] = useState(false);
  const [isForecastEnabled, setForecastEnabled] = useState(true);
  const [isForecastModalOpen, setForecastModalOpen] = useState(false);
  const [products, setProducts] = useState([]);
  const [selectedProducts, setSelectedProducts] = useState([]);
  const [forecastData, setForecastData] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [category, setCategory] = useState(0);
  const [categories, setCategories] = useState([]);
  
  const [newProduct, setNewProduct] = useState({
    product_id: null,
    name: "",
    category_id: 0,
    rating: 0,
    description: "",
    cost_price: 0,
    selling_price: 0,
    available_stock: 0,
    demand_forecast: 0,
    optimized_price: 0,
  });

  const [isViewMode, setViewMode] = useState(false);

  // Toggle modals
  const toggleAddModal = () => {
    setAddModalOpen(!isAddModalOpen);
  };
  const toggleForecastModal = () => setForecastModalOpen(!isForecastModalOpen);
  const toggleForecast = () => setForecastEnabled(!isForecastEnabled);

  // Handle product selection for forecast
  const handleProductSelection = (product) => {
    const isSelected = selectedProducts.some(p => p.product_id === product.product_id);
    if(isSelected){
      setSelectedProducts(selectedProducts.filter(p => p.product_id !== product.product_id));
    }else{
      setSelectedProducts([...selectedProducts, product]);
    }
  };

  // Fetch forecast data
  const fetchForecastData = async () => {
    const demand = selectedProducts.map(p => p.pricing.demand_forecast);
    const price = selectedProducts.map(p => p.pricing.selling_price);
    const product_name = selectedProducts.map(p => p.name);
    console.log(demand,price);
    const chartData = {
    data:{
        labels: product_name,
        datasets: [
          {
            label: 'Product Demand',
            data: demand || [],
            borderColor: "#9370DB", // Purple line color
        backgroundColor: "rgba(147, 112, 219, 0.2)", // Transparent purple fill
        tension: 0.4, // Curved lines


          },
          {
            label: 'Selling Price',
            data: price || [],
            borderColor: "#00FFFF", // Cyan line color
        backgroundColor: "rgba(0, 255, 255, 0.2)", // Transparent cyan fill
        tension: 0.4, // Curved lines


          }
        ],
      },   options : {
        responsive: true,
        plugins: {
          legend: {
            position: "top", // Position of the legend
            labels: {
              color: "#FFFFFF", // Legend text color
            },
          },
          title: {
            display: true,
            text: "Demand Forecast vs Selling Price", // Title of the chart
            color: "#FFFFFF", // Title text color
          },
        },
        scales: {
          x: {
            grid: {
              color: "#444444", // Grey grid lines
            },
            ticks: {
              color: "#FFFFFF", // X-axis label color
            },
            title: {
              display: true,
              text: "Years", // X-axis title
              color: "#FFFFFF", // X-axis title color
            },
          },
          y: {
            grid: {
              color: "#444444", // Grey grid lines
            },
            ticks: {
              color: "#FFFFFF", // Y-axis label color
            },
            title: {
              display: true,
              text: "Values", // Y-axis title
              color: "#FFFFFF", // Y-axis title color
            },
          },
        },
        layout: {
          padding: 20, // Add padding around the chart
        },
      }   
    }
      setForecastData(chartData);
      toggleForecastModal();
    console.log(chartData);
      
  };

  // Fetch products from API
  const fetchProducts = async (search = "", category_id = 0) => {
    try {
        
      const response = await axios.get(`${BASE_URL}/api/products`, {
        params: { search, category_id },
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      if (response.status === 200) {
        setProducts(response.data?.data);
      }
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };

  // Fetch categories from API
  const fetchCategories = async () => {
    try {
      const response = await axios.get(`${BASE_URL}/api/categories`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      if (response.status === 200) {
        setCategories([...response.data?.data]);
        setNewProduct({...newProduct, category_id: response.data?.data[0].category_id});
      }
    } catch (error) {
      console.error("Error fetching categories:", error);
    }
  };

  useEffect(() => {
    fetchCategories(); // Fetch categories on component mount
  }, []);

  function debounce(func, wait) {
    let timeout;
    return function(...args) {
      const context = this;
      clearTimeout(timeout);
      timeout = setTimeout(() => func.apply(context, args), wait);
    };
  }

 
  const debouncedFetchProducts = debounce((search, category) => {
    fetchProducts(search, category);
  }, 1000);

  useEffect(() => {
    debouncedFetchProducts(searchTerm, category);
  }, [searchTerm, category]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewProduct({ ...newProduct, [name]: value });
  };

  const addProduct = async () => {
    try {
      const response = await axios.post(`${BASE_URL}/api/products`, newProduct, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
      if (response.status === 201) {
        setProducts([...products,response.data?.data]);
        toggleAddModal(); // Close the modal
      }
    } catch (error) {
      console.error("Error adding product:", error);
    }
  };

  const handleDelete = async (product_id) => {
    try {
        const response = await axios.delete(`${BASE_URL}/api/products/${product_id}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        if (response.status === 200) {
            setProducts(products.filter(product => product.product_id !== product_id));
            console.log(`Product with ID ${product_id} deleted successfully.`);
        }
    } catch (error) {
        alert(error.response.data?.message);
        console.error("Error deleting product:", error);
    }
  };

  const editProduct = async () => {
    try {
      const updatedProduct = {
        ...newProduct, 
        
      };

      const response = await axios.put(`${BASE_URL}/api/products/${updatedProduct?.product_id}`, updatedProduct, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.status === 200) {
        
        setProducts(products.map(product => 
          product.product_id === updatedProduct?.product_id ? response.data?.data : product
        ));
        console.log(`Product with ID ${updatedProduct?.product_id} updated successfully.`);
        toggleAddModal(); // Close the modal
      }
    } catch (error) {
      console.error("Error updating product:", error);
    }
  };
  const handleEdit = async (product_id) => {
    await handleView(product_id);
    setViewMode(false);
  }


  const handleView = async (product_id) => {
  const response = await axios.get(`${BASE_URL}/api/products/${product_id}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (response.status === 200) {
    console.log("Product details:", response.data?.data);
    let product_data = {
        product_id: response.data?.data.product_id,
        name: response.data?.data.name,
        category_id: response.data?.data.category_id,
        rating: response.data?.data.rating,
        description: response.data?.data.description,
        cost_price: response.data?.data.pricing.cost_price,
        selling_price: response.data?.data.pricing.selling_price,
        available_stock: response.data?.data.stock.available_stock,
        demand_forecast: response.data?.data.pricing.demand_forecast,
        optimized_price: response.data?.data.optimized_price.optimized_price,
    }
    setNewProduct(product_data);
    toggleAddModal();
    setViewMode(true);
    
  } else {
    alert(response.data?.message);
    console.error("Error fetching product details:", response.status);
  }
  };
  const handleAdd = () => {
    toggleAddModal();
    setViewMode(false);
    setNewProduct({
      product_id: null,
      name: "",
      category_id: 0,
      rating: 0,
      description: "",
      cost_price: 0,
      selling_price: 0,
      available_stock: 0,
      demand_forecast: 0,
      optimized_price: 0,
    });
  }

  return (
    <div className="manage-product-container">
      <Header />
      <header>
        <h1>MANAGE PRODUCTS</h1>
        <div className="header-actions">
          <FormControlLabel
            control={<Switch checked={isForecastEnabled} onChange={toggleForecast} />}
            label="With Demand Forecast"
          />
          <div className="forecast-button">
            <Button
              variant="contained"
              color="primary"
              onClick={fetchForecastData}
              disabled={selectedProducts.length === 0}
            >
              View Forecast
            </Button>
            </div>
          
        </div>
      </header>

      <div className="actions-bar">
        <TextField
          placeholder="Search"
          variant="outlined"
          size="small"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <Select
          variant="outlined"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          size="small"
        >
          <MenuItem value={0}>All Categories</MenuItem>
          {categories.map((cat) => (
            <MenuItem key={cat.id} value={cat.category_id}>
              {cat.name}
            </MenuItem>
          ))}
        </Select>
        <Button variant="contained" onClick={handleAdd}>
          <AddIcon /> Add New Product
        </Button>
      </div>

      {isForecastEnabled && (
        <div className="selection-info">
          <p>Select products to view demand forecast</p>
          <p>Selected: {selectedProducts.length} products</p>
        </div>
      )}

      <ProductTable
        products={products}
        isForecastEnabled={isForecastEnabled}
        handleDelete={handleDelete}
        handleEdit={handleEdit}
        handleView={handleView}
        selectedProducts={selectedProducts}
        onProductSelect={handleProductSelection}
      />

      {/* Add Product Modal */}
      <Modal isOpen={isAddModalOpen} onRequestClose={toggleAddModal} className="modal">
        <h2>{isViewMode ? "View Product" : "Add New Product"}</h2>
        <form className="modal-form">
          <TextField
            label="Product Name"
            variant="outlined"
            fullWidth
            margin="normal"
            name="name"
            value={newProduct.name}
            onChange={handleInputChange}
            disabled={isViewMode}
          />
         
          <TextField
            label="Cost Price"
            variant="outlined"
            fullWidth
            margin="normal"
            name="cost_price"
            type="number"
            value={newProduct.cost_price}
            onChange={handleInputChange}
            disabled={isViewMode}
          />
          <TextField
            label="Selling Price"
            variant="outlined"
            fullWidth
            margin="normal"
            name="selling_price"
            type="number"
            value={newProduct.selling_price}
            onChange={handleInputChange}
            disabled={isViewMode}
          />
          <TextField
            label="Description"
            variant="outlined"
            fullWidth
            margin="normal"
            multiline
            rows={1}
            name="description"
            value={newProduct.description}
            onChange={handleInputChange}
            disabled={isViewMode}
          />
          <TextField
            label="Available Stock"
            variant="outlined"
            fullWidth
            margin="normal"
            name="available_stock"
            type="number"
            value={newProduct.available_stock}
            onChange={handleInputChange}
            disabled={isViewMode}
          />
          <TextField
            label="Optimized Price"
            variant="outlined"
            fullWidth
            margin="normal"
            name="optimized_price"
            type="number"
            value={newProduct.optimized_price}
            onChange={handleInputChange}
            disabled={isViewMode}
          />
            <TextField
            label="Demand Forecast"
            variant="outlined"
            fullWidth
            margin="normal"
            name="demand_forecast"
            type="number"
            value={newProduct.demand_forecast}
            onChange={handleInputChange}
            disabled={isViewMode}
            />
          <Select
            label="Product Category"
            variant="outlined"
            fullWidth
            margin="normal"
            name="category_id"
            value={newProduct.category_id}
            onChange={handleInputChange}
            disabled={isViewMode}
          >
            {categories.map((cat) => (
              <MenuItem key={cat.category_id} value={cat.category_id} >
                {cat.name}
              </MenuItem>
            ))}
          </Select>
          <div className="modal-actions">
            <Button variant="outlined" onClick={() => { toggleAddModal(); setViewMode(false); }}>
              Close
            </Button>
            {!isViewMode && (
              <Button variant="contained" color="primary" onClick={newProduct?.product_id ? editProduct : addProduct}>
                {newProduct.product_id ? "Edit" : "Add"}
              </Button>
            )}
          </div>
        </form>
      </Modal>

      {/* Demand Forecast Modal */}
      <DemandForecastModal
        isOpen={isForecastModalOpen}
        chartData={forecastData}
        onClose={toggleForecastModal}
        selectedProducts={selectedProducts}
      />
    </div>
  );
};

export default CreateManageProduct;
