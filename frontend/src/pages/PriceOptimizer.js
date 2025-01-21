import React, { useState, useEffect } from "react";
import { Button, TextField, Select, MenuItem, Switch, FormControlLabel } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import Modal from "react-modal";
import ProductTable from "../components/ProductTable/ProductTable";
import Header from "../components/Header/Header";
import axios from "axios";
import { useAuth } from "../context/AuthContext";
import { BASE_URL } from "../config";

const CreateManageProduct = () => {
  const { token } = useAuth();
  const [isOptimizedPriceEnabled, setOptimizedPriceEnabled] = useState(false);
  const [products, setProducts] = useState([]);
  const [category, setCategory] = useState(0);
  const [categories, setCategories] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");

  
  const [newProduct, setNewProduct] = useState({})


  // Fetch products from API
  const fetchProducts = async (search = "", category_id = 0, is_optimised_price = true) => {
    try {
        
      const response = await axios.get(`${BASE_URL}/api/products`, {
        params: { search, category_id, is_optimised_price },
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

  
const toggleOptimizedPrice = () => {
  setOptimizedPriceEnabled(!isOptimizedPriceEnabled);
}

 



  return (
    <div className="manage-product-container">
        <Header />
      <header>
        <h1>MANAGE PRODUCTS</h1>
        <FormControlLabel
          control={<Switch checked={isOptimizedPriceEnabled } onChange={toggleOptimizedPrice} />}
          label="With Optimized Price"
        />
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
       
       
      </div>

      <ProductTable products={products}  isOptimizedPriceEnabled={isOptimizedPriceEnabled}  />

      {/* Remove Add Product Modal */}
    </div>
  );
};

export default CreateManageProduct;
