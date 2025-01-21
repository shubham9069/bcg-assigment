import React, { useCallback, useMemo } from "react";
import "./ProductTable.css";
import { IconButton, Checkbox } from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import VisibilityIcon from "@mui/icons-material/Visibility";

const ProductTable = ({
  products = [],
  isForecastEnabled = false,
  handleDelete,
  handleEdit,
  handleView,
  selectedProducts = [],
  onProductSelect,
  isOptimizedPriceEnabled = false
}) => {
  const buttonActions = useMemo(() => {
    if (handleView || handleEdit || handleDelete) {
      return true;
    }
    return false;
  }, [handleView, handleEdit, handleDelete]);

  const isSelected =useCallback((product)=>{
    return selectedProducts.some(p => p.product_id === product.product_id);
  },[selectedProducts])

  return (
    <table className="product-table">
      <thead>
        <tr>
          {onProductSelect && <th>Select</th>}
          <th>Product Name</th>
          <th>Product Category</th>
          <th>Cost Price</th>
          <th>Selling Price</th>
          <th>Description</th>
          <th>Available Stock</th>
          <th>Units Sold</th>
          {isForecastEnabled && <th>Demand Forecast</th>}
          {isOptimizedPriceEnabled && <th>Optimized Price</th>}
          {buttonActions && <th>Action</th>}
        </tr>
      </thead>
      <tbody>
        {products.map((product) => (
          <tr key={product.product_id} className={isSelected(product) ? 'selected-row' : ''}>
            {onProductSelect && (
              <td>
                <Checkbox
                  checked={isSelected(product)}
                  onChange={() => onProductSelect(product)}
                  color="primary"
                />
              </td>
            )}
            <td>{product.name}</td>
            <td>{product.category.category_name}</td>
            <td>{product.pricing.cost_price}</td>
            <td>{product.pricing.selling_price}</td>
            <td className="test-overflow">{product.description}</td>
            <td>{product.stock.available_stock}</td>
            <td>{product.stock.units_sold}</td>
            {isForecastEnabled && <td>{product.pricing.demand_forecast}</td>}
            {isOptimizedPriceEnabled && <td>{product.optimized_price.optimized_price}</td>}
            {buttonActions && (
              <td>
                {handleView && (
                  <IconButton onClick={() => handleView(product.product_id)}>
                    <VisibilityIcon />
                  </IconButton>
                )}
                {handleEdit && (
                  <IconButton onClick={() => handleEdit(product.product_id)}>
                    <EditIcon />
                  </IconButton>
                )}
                {handleDelete && (
                  <IconButton onClick={() => handleDelete(product.product_id)}>
                    <DeleteIcon />
                  </IconButton>
                )}
              </td>
            )}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default ProductTable;
