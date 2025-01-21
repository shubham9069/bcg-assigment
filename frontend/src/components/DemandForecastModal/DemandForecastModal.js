import React from 'react';
import Modal from 'react-modal';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import './DemandForecastModal.css';
import ProductTable from '../ProductTable/ProductTable';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const DemandForecastModal = ({ chartData, isOpen, onClose, selectedProducts }) => {
  
console.log(chartData);


  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onClose}
      className="forecast-modal"
      overlayClassName="forecast-modal-overlay"
    >
      <div className="forecast-modal-content">
        <h2>Demand Forecast</h2>

        <div className="chart-container">
          <Line data={chartData?.data} options={chartData?.options} />
        </div>

        <ProductTable products={selectedProducts} isForecastEnabled={true} />
       
        <button className="close-button" onClick={onClose}>
          Close
        </button>
      </div>
    </Modal>
  );
};

export default DemandForecastModal; 