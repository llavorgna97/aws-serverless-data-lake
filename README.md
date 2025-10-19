# ☁️ AWS Serverless Data Lake Project

This repository showcases a **serverless data lake pipeline** built entirely with **AWS native services**.  
It includes three AWS Lambda functions that generate, process, and analyze synthetic e-commerce data.  

The project is inspired by the AWS Training & Certification lab *“Setting up a Data Lake on AWS (v1.0.4)”*,  
but fully rewritten with custom logic and configurations for educational purposes.

---

## 🧩 Architecture Overview

The solution is organized into three S3 zones managed by Lambda functions:

| Zone | Function | Description |
|------|-----------|--------------|
| **Raw Zone** | `data_generator.py` | Creates and uploads simulated cart abandonment data. |
| **Processing Zone** | `data_processor.py` | Aggregates raw data by product ID and summarizes cart behavior. |
| **Consumption Zone** | `promotion_app.py` | Identifies top abandoned products per customer for promotional targeting. |

**AWS Services Used**
- **Amazon S3** – Object storage and data layer separation  
- **AWS Lambda** – Serverless compute for ETL operations  
- **Amazon EventBridge** – (Optional) Orchestration and automation between functions  

---

## ⚙️ Workflow Summary

1. **Data Generation**  
   The `data_generator.py` Lambda produces 1,000 fake cart entries using the **Faker** library.  
   Each record includes customer, product, and pricing details. The file is uploaded to the S3 **input bucket**.

2. **Data Processing**  
   The `data_processor.py` Lambda reads the raw CSV file from S3,  
   aggregates the product quantities, and writes a summary CSV of the top 50 most abandoned products.

3. **Promotion App**  
   The `promotion_app.py` Lambda analyzes customer-product interactions  
   and extracts the top 10 abandoned items per customer, exporting results to the **output bucket**.

---

## 🧰 Technologies

| Category | Tools |
|-----------|-------|
| Cloud | AWS Lambda, Amazon S3, Amazon EventBridge |
| Programming | Python (Faker, Pandas, Boto3) |
| Data Zones | Raw → Processed → Consumption |
| Architecture | Event-driven Serverless Data Lake |
